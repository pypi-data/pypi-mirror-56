##
# Spiking layers with JAX backend
#

# - Imports
from ..layer import Layer
from ...timeseries import TSContinuous, TSEvent

from jax import numpy as np
import numpy as onp

from jax import jit, custom_gradient
from jax.lax import scan
import jax.random as rand

from typing import Optional, Tuple, Union, Dict, Callable

# - Define a float / array type
FloatVector = Union[float, np.ndarray]

# - Define a layer state type
LayerState = Dict[
    str, np.ndarray
]  # TypedDict("LayerState", {"spikes": np.ndarray, "Imem": np.ndarray, "Vmem": np.ndarray})

# - Define module exports
__all__ = ["RecLIFJax", "RecLIFCurrentInJax", "RecLIFJax_IO"]


def _evolve_lif_jax(
    state0: LayerState,
    w_in: np.ndarray,
    w_rec: np.ndarray,
    w_out_surrogate: np.ndarray,
    tau_mem: np.ndarray,
    tau_syn: np.ndarray,
    bias: np.ndarray,
    noise_std: float,
    sp_input_ts: np.ndarray,
    I_input_ts: np.ndarray,
    key: int,
    dt: float,
) -> (
    LayerState,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
):
    """
    Raw JAX evolution function for an LIF spiking layer

    This function implements the dynamics:

    .. math ::

        \\tau_{syn} \dot{I}_{syn} + I_{syn} = 0

        I_{syn} += S_{in}(t)

        \\tau_{syn} \dot{V}_{mem} + V_{mem} = I_{syn} + b + \sigma\zeta(t)

    where :math:`S_{in}(t)` is a vector containing ``1`` for each input channel that emits a spike at time :math:`t`; :math:`b` is a :math:`N` vector of bias currents for each neuron; :math:`\\sigma\\zeta(t)` is a white-noise process with standard deviation :math:`\\sigma` injected independently onto each neuron's membrane; and :math:`\\tau_{mem}` and :math:`\\tau_{syn}` are the membrane and synaptic time constants, respectively.

    :On spiking:

    When the membane potential for neuron :math:`j`, :math:`V_{mem, j}` exceeds the threshold voltage :math:`V_{thr} = 0`, then the neuron emits a spike.

    .. math ::

        V_{mem, j} > V_{thr} \\rightarrow S_{rec,j} = 1

        I_{syn} = I_{syn} + S_{rec} \cdot w_{rec}

        V_{mem, j} = V_{mem, j} - 1

    Neurons therefore share a common resting potential of ``0``, a firing threshold of ``0``, and a subtractive reset of ``-1``. Neurons each have an optional bias current `.bias` (default: ``-1``).

    :Surrogate signals:

    To facilitate gradient-based training, a surrogate :math:`U(t)` is generated from the membrane potentials of each neuron.

    .. math ::

        U_j = \\textrm{sig}(V_j)

    :param LayerState state0:           Layer state at start of evolution
    :param np.ndarray w_in:             Input weights [I, N]
    :param np.ndarray w_rec:            Recurrent weights [N, N]
    :param np.ndarray w_out_surrogate:  Output weights [N, O]
    :param np.ndarray tau_mem:          Membrane time constants for each neuron [N,]
    :param np.ndarray tau_syn:          Input synapse time constants for each neuron [N,]
    :param np.ndarray bias:             Bias values for each neuron [N,]
    :param float noise_std:             Noise injected onto the membrane of each neuron. Standard deviation at each time step.
    :param np.ndarray sp_input_ts:      Logical spike raster of input events on input channels [T, I]
    :param np.ndarray I_input_ts:       Time trace of currents injected on input channels (direct current injection) [T, I]
    :param int key:                     pRNG key for JAX
    :param float dt:                    Time step in seconds

    :return: (state, Irec_ts, output_ts, surrogate_ts, spikes_ts, Vmem_ts, Isyn_ts)
        state:          (LayerState) Layer state at end of evolution
        Irec_ts:        (np.ndarray) Recurrent input received at each neuron over time [T, N]
        output_ts:      (np.ndarray) Weighted output surrogate over time [T, O]
        surrogate_ts:   (np.ndarray) Surrogate time trace for each neuron [T, N]
        spikes_ts:      (np.ndarray) Logical spiking raster for each neuron [T, N]
        Vmem_ts:        (np.ndarray) Membrane voltage of each neuron over time [T, N]
        Isyn_ts:        (np.ndarray) Synaptic input current received by each neuron over time [T, N]
    """

    # - Get evolution constants
    alpha = dt / tau_mem
    beta = np.exp(-dt / tau_syn)

    # - Surrogate functions to use in learning
    def sigmoid(x: FloatVector) -> FloatVector:
        """
        Sigmoid function

        :param FloatVector x: Input value

        :return FloatVector: Output value
        """
        return 1 / (1 + np.exp(-x))

    @custom_gradient
    def step_pwl(x: FloatVector) -> (FloatVector, Callable[[FloatVector], FloatVector]):
        """
        Heaviside step function with piece-wise linear derivative to use as spike-generation surrogate

        :param FloatVector x: Input value

        :return (FloatVector, Callable[[FloatVector], FloatVector]): output value and gradient function
        """
        s = np.clip(np.floor(x + 1.0), 0.0)
        return s, lambda g: (g * (x > -0.5),)

    # - Single-step LIF dynamics
    def forward(
        state: LayerState, inputs_t: Tuple[np.ndarray, np.ndarray]
    ) -> (
        LayerState,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ):
        """
        Single-step LIF dynamics for a recurrent LIF layer

        :param LayerState state:
        :param Tuple[np.ndarray, np.ndarray] inputs_t: (spike_inputs_ts, current_inputs_ts)

        :return: (state, Irec_ts, output_ts, surrogate_ts, spikes_ts, Vmem_ts, Isyn_ts)
            state:          (LayerState) Layer state at end of evolution
            Irec_ts:        (np.ndarray) Recurrent input received at each neuron over time [T, N]
            output_ts:      (np.ndarray) Weighted output surrogate over time [T, O]
            surrogate_ts:   (np.ndarray) Surrogate time trace for each neuron [T, N]
            spikes_ts:      (np.ndarray) Logical spiking raster for each neuron [T, N]
            Vmem_ts:        (np.ndarray) Membrane voltage of each neuron over time [T, N]
            Isyn_ts:        (np.ndarray) Synaptic input current received by each neuron over time [T, N]
        """
        # - Unpack inputs
        (sp_in_t, I_in_t) = inputs_t
        sp_in_t = sp_in_t.reshape(-1)
        Iin = I_in_t.reshape(-1)

        # - Synaptic input
        Irec = np.dot(state["spikes"], w_rec)
        dIsyn = sp_in_t + Irec
        state["Isyn"] = beta * state["Isyn"] + dIsyn

        # - Apply subtractive reset
        state["Vmem"] = state["Vmem"] - state["spikes"]

        # - Membrane potentials
        dVmem = state["Isyn"] + Iin + bias - state["Vmem"]
        state["Vmem"] = state["Vmem"] + alpha * dVmem

        # - Detect next spikes (with custom gradient)
        state["spikes"] = step_pwl(state["Vmem"])

        # - Return state and outputs
        return state, (Irec, state["spikes"], state["Vmem"], state["Isyn"])

    # - Generate membrane noise trace
    # - Build noise trace
    # - Compute random numbers for reservoir noise
    num_timesteps = sp_input_ts.shape[0]
    __all__, subkey = rand.split(key)
    noise_ts = noise_std * rand.normal(
        subkey, shape=(num_timesteps, np.size(state0["Vmem"]))
    )

    # - Evolve over spiking inputs
    state, (Irec_ts, spikes_ts, Vmem_ts, Isyn_ts) = scan(
        forward,
        state0,
        (np.dot(sp_input_ts, w_in), np.dot(I_input_ts, w_in) + noise_ts),
    )

    # - Generate output surrogate
    surrogate_ts = sigmoid(Vmem_ts)

    # - Weighted output
    output_ts = np.dot(surrogate_ts, w_out_surrogate)

    # - Return outputs
    return state, Irec_ts, output_ts, surrogate_ts, spikes_ts, Vmem_ts, Isyn_ts


class RecLIFJax(Layer):
    """
    Recurrent spiking neuron layer (LIF), spiking input and spiking output. No input / output weights.

    `.RecLIFJax` is a basic recurrent spiking neuron layer, implemented with a JAX-backed Euler solver backend. Outputs are spikes generated by each layer neuron; no output weighting is provided. Inputs are provided by spiking through a synapse onto each layer neuron; no input weighting is provided. The layer is therefore N inputs -> N neurons -> N outputs.

    This layer can be used to implement gradient-based learning systems, using the JAX-provided automatic differentiation functionality of `jax.grad`.

    :Dynamics:

    The dynamics of the :math:`N` neurons' membrane potential :math:`V_{mem}` and the :math:`N` synaptic currents :math:`I_{syn}` evolve under the system

    .. math::

        \\tau_{syn} \dot{I}_{syn} + I_{syn} = 0

        I_{syn} += S_{in}(t)

        \\tau_{syn} \dot{V}_{mem} + V_{mem} = I_{syn} + b + \sigma\zeta(t)

    where :math:`S_{in}(t)` is a vector containing ``1`` for each input channel that emits a spike at time :math:`t`; :math:`b` is a :math:`N` vector of bias currents for each neuron; :math:`\\sigma\\zeta(t)` is a white-noise process with standard deviation :math:`\\sigma` injected independently onto each neuron's membrane; and :math:`\\tau_{mem}` and :math:`\\tau_{syn}` are the membrane and synaptic time constants, respectively.

    :On spiking:

    When the membane potential for neuron :math:`j`, :math:`V_{mem, j}` exceeds the threshold voltage :math:`V_{thr} = 0`, then the neuron emits a spike.

    .. math ::

        V_{mem, j} > V_{thr} \\rightarrow S_{rec,j} = 1

        I_{syn} = I_{syn} + S_{rec} \cdot w_{rec}

        V_{mem, j} = V_{mem, j} - 1

    Neurons therefore share a common resting potential of ``0``, a firing threshold of ``0``, and a subtractive reset of ``-1``. Neurons each have an optional bias current `.bias` (default: ``-1``).

    :Surrogate signals:

    To facilitate gradient-based training, a surrogate :math:`U(t)` is generated from the membrane potentials of each neuron.

    .. math ::

        U_j = \\textrm{sig}(V_j)

    Where :math:`\\textrm{sig}(x) = \\left(1 + \\exp(-x)\\right)^{-1}`.

    :Outputs from evolution:

    As output, this layer returns the spiking activity of the :math:`N` neurons from the `.evolve` method. After each evolution, the attributes `.spikes_last_evolution`, `.i_rec_last_evolution` and `.v_mem_last_evolution` and `.surrogate_last_evolution` will be `.TimeSeries` objects containing the appropriate time series.
    """

    def __init__(
        self,
        w_recurrent: np.ndarray,
        tau_mem: FloatVector,
        tau_syn: FloatVector,
        bias: Optional[FloatVector] = -1.0,
        noise_std: Optional[float] = 0.0,
        dt: Optional[float] = None,
        name: Optional[str] = None,
        rng_key: Optional[int] = None,
    ):
        """
        A basic recurrent spiking neuron layer, with a JAX-implemented forward Euler solver.

        :param ndarray w_recurrent:                     [N,N] Recurrent weight matrix
        :param ArrayLike[float] tau_mem:                [N,] Membrane time constants
        :param ArrayLike[float] tau_syn:                [N,] Output synaptic time constants
        :param Optional[ArrayLike[float]] bias:         [N,] Bias currents for each neuron (Default: 0)
        :param Optional[float] noise_std:               Std. dev. of white noise injected independently onto the membrane of each neuron (Default: 0)
        :param Optional[float] dt:                      Forward Euler solver time step. Default: min(tau_mem, tau_syn) / 10
        :param Optional[str] name:                      Name of this layer. Default: `None`
        :param Optional[int] rng_key:                   JAX pRNG key. Default: generate a new key
        """
        # - Ensure that weights are 2D
        w_recurrent = np.atleast_2d(w_recurrent)

        # - Transform arguments to JAX np.array
        tau_mem = np.array(tau_mem)
        tau_syn = np.array(tau_syn)
        bias = np.array(bias)

        if dt is None:
            dt = np.min(np.array((np.min(tau_mem), np.min(tau_syn)))) / 10.0

        # - Call super-class initialisation
        super().__init__(w_recurrent, dt, noise_std, name)

        # - Set properties
        self.tau_mem = tau_mem
        self.tau_syn = tau_syn
        self.bias = bias

        self._w_in = 1
        self._w_out = 1

        # - Get compiled evolution function
        self._evolve_jit = jit(_evolve_lif_jax)

        # - Initialise "last evolution" attributes
        self.v_mem_last_evolution = None
        self.spikes_last_evolution = None

        # - Reset layer state
        self.reset_all()

        # - Seed RNG
        if rng_key is None:
            rng_key = rand.PRNGKey(onp.random.randint(0, 2 ** 63))
        _, self._rng_key = rand.split(rng_key)

    def reset_state(self):
        """
        Reset the membrane potentials, synaptic currents and refractory state for this layer
        """
        self._state = {
            "Vmem": np.zeros((self._size,)),
            "Isyn": np.zeros((self._size,)),
            "spikes": np.zeros((self._size,)),
        }

    def evolve(
        self,
        ts_input: Optional[TSEvent] = None,
        duration: Optional[float] = None,
        num_timesteps: Optional[int] = None,
        verbose: Optional[bool] = False,
    ) -> TSEvent:
        """
        Evolve the state of this layer given an input

        :param Optional[TSEvent] ts_input:      Input time series. Default: `None`, no stimulus is provided
        :param Optional[float] duration:        Simulation/Evolution time, in seconds. If not provided, then `num_timesteps` or the duration of `ts_input` is used to determine evolution time
        :param Optional[int] num_timesteps:     Number of evolution time steps, in units of `.dt`. If not provided, then `duration` or the duration of `ts_input` is used to determine evolution time
        :param Optional[bool]verbose:           Currently no effect, just for conformity

        :return TSContinuous:                   Output time series; the synaptic currents of each neuron
        """

        # - Prepare time base and inputs
        time_base, inps, num_timesteps = self._prepare_input_events(
            ts_input, duration, num_timesteps
        )

        # - Call raw evolution function
        time_start = self.t
        Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts = self._evolve_raw(
            inps, inps * 0.0
        )

        # - Record membrane traces
        self.v_mem_last_evolution = TSContinuous(time_base, onp.array(Vmem_ts))

        # - Record spike raster
        spikes_ids = onp.argwhere(onp.array(spike_raster_ts))
        self.spikes_last_evolution = TSEvent(
            spikes_ids[:, 0] * self.dt + time_start,
            spikes_ids[:, 1],
            t_start=time_start,
            t_stop=self.t,
            name="Spikes " + self.name,
            num_channels=self.size,
        )

        # - Record neuron surrogates
        self.surrogate_last_evolution = TSContinuous(time_base, onp.array(surrogate_ts))

        # - Record recurrent inputs
        self.i_rec_last_evolution = TSContinuous(time_base, onp.array(Irec_ts))

        # - Record synaptic currents
        self.i_syn_last_evolution = TSContinuous(time_base, onp.array(Isyn_ts))

        # - Wrap spiking outputs as time series
        return self.spikes_last_evolution

    def _evolve_raw(
        self, sp_input_ts: np.ndarray, I_input_ts: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Raw evolution over an input array

        :param ndarray sp_input_ts:     Input matrix [T, I]
        :param ndarray I_input_ts:      Input matrix [T, N]

        :return:  (Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts)
                Irec_ts:         (np.ndarray) Time trace of recurrent current inputs per neuron [T, N]
                output_ts:       (np.ndarray) Time trace of surrogate weighted output [T, O]
                surrogate_ts:    (np.ndarray) Time trace of surrogate from each neuron [T, N]
                spike_raster_ts: (np.ndarray) Boolean raster [T, N]; `True` if a spike occurred in time step `t`, from neuron `n`
                Vmem_ts:         (np.ndarray) Time trace of neuron membrane potentials [T, N]
                Isyn_ts:         (np.ndarray) Time trace of output synaptic currents [T, N]
        """
        # - Call compiled Euler solver to evolve reservoir
        self._state, Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts = self._evolve_jit(
            self._state,
            self._w_in,
            self._weights,
            self._w_out,
            self._tau_mem,
            self._tau_syn,
            self._bias,
            self._noise_std,
            sp_input_ts,
            I_input_ts,
            self._rng_key,
            self._dt,
        )

        # - Increment timesteps attribute
        self._timestep += sp_input_ts.shape[0] - 1

        # - Return layer activity
        return Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts

    def to_dict(self) -> dict:
        """
        Convert the configuration of this layer into a dictionary to assist in reconstruction

        :return: dict
        """
        config = super().to_dict()
        config["tau_mem"] = self.tau_mem.tolist()
        config["tau_syn"] = self.tau_syn.tolist()
        config["bias"] = self.bias.tolist()
        config["rng_key"] = self._rng_key.tolist()
        return config

    @property
    def w_recurrent(self) -> np.ndarray:
        """ (ndarray) Recurrent weight matrix [N, N] """
        return onp.array(self._weights)

    @w_recurrent.setter
    def w_recurrent(self, value: np.ndarray):
        assert np.ndim(value) == 2, "`w_recurrent` must be 2D"

        assert value.shape == (
            self._size,
            self._size,
        ), "`w_recurrent` must be [{:d}, {:d}]".format(self._size, self._size)

        self._weights = np.array(value).astype("float32")

    @property
    def tau_mem(self) -> np.ndarray:
        """ (ndarray) Membrane time constant for each neuron [N,] """
        return onp.array(self._tau_mem)

    @tau_mem.setter
    def tau_mem(self, value: np.ndarray):
        # - Replicate `tau_mem` from a scalar value
        if np.size(value) == 1:
            value = np.repeat(value, self._size)

        assert (
            np.size(value) == self._size
        ), "`tau_mem` must have {:d} elements or be a scalar".format(self._size)

        # - Check for valid time constant
        assert np.all(value > 0.0), "`tau_mem` must be larger than zero"

        if hasattr(self, "dt"):
            tau_min = self.dt * 10.0
            assert np.all(
                value >= tau_min
            ), "`tau_mem` must be larger than {:4f}".format(tau_min)

        self._tau_mem = np.reshape(value, self._size).astype("float32")

    @property
    def tau_syn(self) -> np.ndarray:
        """ (ndarray) Output synaptic time constant for each neuron [N,] """
        return onp.array(self._tau_syn)

    @tau_syn.setter
    def tau_syn(self, value: np.ndarray):
        # - Replicate `tau_syn` from a scalar value
        if np.size(value) == 1:
            value = np.repeat(value, self._size)

        assert (
            np.size(value) == self._size
        ), "`tau_syn` must have {:d} elements or be a scalar".format(self._size)

        # - Check for valid time constant
        assert np.all(value > 0.0), "`tau_syn` must be larger than zero"

        if hasattr(self, "dt"):
            tau_min = self.dt * 10.0
            assert np.all(
                value >= tau_min
            ), "`tau_syn` must be larger than {:4f}".format(tau_min)

        self._tau_syn = np.reshape(value, self._size).astype("float32")

    @property
    def bias(self) -> np.ndarray:
        """ (ndarray) Bias current for each neuron [N,] """
        return onp.array(self._bias)

    @bias.setter
    def bias(self, value: np.ndarray):
        # - Replicate `bias` from a scalar value
        if np.size(value) == 1:
            value = np.repeat(value, self._size)

        assert (
            np.size(value) == self._size
        ), "`bias` must have {:d} elements or be a scalar".format(self._size)

        self._bias = np.reshape(value, self._size).astype("float32")

    @property
    def dt(self) -> float:
        """ (float) Forward Euler solver time step """
        return onp.array(self._dt).item(0)

    @dt.setter
    def dt(self, value: float):
        """ (float) Time step in seconds """
        # - Ensure dt is numerically stable
        tau_min = np.min(np.min(self._tau_mem), np.min(self._tau_syn)) / 10.0
        if value is None:
            value = tau_min

        # - Check for valid time constant
        assert np.all(value > 0.0), "`dt` must be larger than zero"
        assert value >= tau_min, "`dt` must be at least {:.2e}".format(tau_min)

        self._dt = np.array(value).astype("float32")

    @property
    def output_type(self):
        """ (TSEvent) Output `.TimeSeries` class: `.TSEvent` """
        return TSEvent

    @property
    def input_type(self):
        """ (TSEvent) Input `.TimeSeries` class: `.TSEvent` """
        return TSEvent


class RecLIFCurrentInJax(RecLIFJax):
    """
    Recurrent spiking neuron layer (LIF), current injection input and spiking output. No input / output weights.

    `.RecLIFCurrentInJax` is a basic recurrent spiking neuron layer, implemented with a JAX-backed Euler solver backend. Outputs are spikes generated by each layer neuron; no output weighting is provided. Inputs are provided by direct current injection onto each neuron membrane; no input weighting is provided. The layer is therefore N inputs -> N neurons -> N outputs.

    This layer can be used to implement gradient-based learning systems, using the JAX-provided automatic differentiation functionality of `jax.grad`.

    :Dynamics:

    The dynamics of the :math:`N` neurons' membrane potential :math:`V_{mem}` and the :math:`N` synaptic currents :math:`I_{syn}` evolve under the system

    .. math::

        \\tau_{syn} \dot{I}_{syn} + I_{syn} = 0

        \\tau_{syn} \dot{V}_{mem} + V_{mem} = I_{syn} + I_{in}(t) + b + \sigma\zeta(t)

    where :math:`S_{in}(t)` is a vector containing ``1`` for each input channel that emits a spike at time :math:`t`; :math:`I_{in}(t)` is a vector of input currents injected directly onto the neuron membranes; :math:`b` is a :math:`N` vector of bias currents for each neuron; :math:`\\sigma\\zeta(t)` is a white-noise process with standard deviation :math:`\\sigma` injected independently onto each neuron's membrane; and :math:`\\tau_{mem}` and :math:`\\tau_{syn}` are the membrane and synaptic time constants, respectively.

    :On spiking:

    When the membane potential for neuron :math:`j`, :math:`V_{mem, j}` exceeds the threshold voltage :math:`V_{thr} = 0`, then the neuron emits a spike.

    .. math ::

        V_{mem, j} > V_{thr} \\rightarrow S_{rec,j} = 1

        I_{syn} = I_{syn} + S_{rec} \cdot w_{rec}

        V_{mem, j} = V_{mem, j} - 1

    Neurons threfore share a common resting potential of ``0``, a firing threshold of ``0``, and a subtractive reset of ``-1``. Neurons each have an optional bias current `.bias` (default: ``-1``).

    :Surrogate signals:

    To facilitate gradient-based training, a surrogate :math:`U(t)` is generated from the membrane potentials of each neuron.

    .. math ::

        U_j = \\textrm{sig}(V_j)

    Where :math:`\\textrm{sig}(x) = \\left(1 + \\exp(-x)\\right)^{-1}`.

    :Outputs from evolution:

    As output, this layer returns the spiking activity of the :math:`N` neurons from the `.evolve` method. After each evolution, the attributes `.spikes_last_evolution`, `.i_rec_last_evolution` and `.v_mem_last_evolution` and `.surrogate_last_evolution` will be `.TimeSeries` objects containing the appropriate time series.
    """

    def evolve(
        self,
        ts_input: Optional[TSContinuous] = None,
        duration: Optional[float] = None,
        num_timesteps: Optional[int] = None,
        verbose: Optional[bool] = False,
    ) -> TSEvent:
        """
        Evolve the state of this layer given an input

        :param Optional[TSContinuous] ts_input: Input time series. Default: `None`, no stimulus is provided
        :param Optional[float] duration:        Simulation/Evolution time, in seconds. If not provided, then `num_timesteps` or the duration of `ts_input` is used to determine evolution time
        :param Optional[int] num_timesteps:     Number of evolution time steps, in units of `.dt`. If not provided, then `duration` or the duration of `ts_input` is used to determine evolution time
        :param Optional[bool] verbose:          Currently no effect, just for conformity

        :return TSEvent:                   Output time series; spiking activity each neuron
        """

        # - Prepare time base and inputs
        time_base, inps, num_timesteps = self._prepare_input(
            ts_input, duration, num_timesteps
        )

        # - Call raw evolution function
        time_start = self.t
        Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts = self._evolve_raw(
            inps * 0.0, inps
        )

        # - Record membrane traces
        self.v_mem_last_evolution = TSContinuous(time_base, onp.array(Vmem_ts))

        # - Record spike raster
        spikes_ids = onp.argwhere(onp.array(spike_raster_ts))
        self.spikes_last_evolution = TSEvent(
            spikes_ids[:, 0] * self.dt + time_start,
            spikes_ids[:, 1],
            t_start=time_start,
            t_stop=self.t,
            name="Spikes " + self.name,
            num_channels=self.size,
        )

        # - Record neuron surrogates
        self.surrogate_last_evolution = TSContinuous(time_base, onp.array(surrogate_ts))

        # - Record recurrent inputs
        self.i_rec_last_evolution = TSContinuous(time_base, onp.array(Irec_ts))

        # - Record synaptic currents
        self.i_syn_last_evolution = TSContinuous(time_base, onp.array(Isyn_ts))

        # - Wrap spiking outputs as time series
        return self.spikes_last_evolution

    @property
    def output_type(self):
        """ (TSEvent) Output `.TimeSeries` class: `.TSEvent` """
        return TSEvent

    @property
    def input_type(self):
        """ (TSContinuous) Output `.TimeSeries` class: `.TSContinuous` """
        return TSContinuous


class RecLIFJax_IO(RecLIFJax):
    """
    Recurrent spiking neuron layer (LIF), spiking input and weighted surrogate output. Input and output weights.

    `.RecLIFJax` is a basic recurrent spiking neuron layer, implemented with a JAX-backed Euler solver backend. Outputs are surrogates generated by each layer neuron, weighted by a set of ourput weights. Inputs are provided by spiking through a synapse onto each layer neuronvia a set of input weights. The layer is therefore M inputs -> N neurons -> O outputs.

    This layer can be used to implement gradient-based learning systems, using the JAX-provided automatic differentiation functionality of `jax.grad`.

    :Dynamics:

    The dynamics of the :math:`N` neurons' membrane potential :math:`V_{mem}` and the :math:`N` synaptic currents :math:`I_{syn}` evolve under the system

    .. math::

        \\tau_{syn} \dot{I}_{syn} + I_{syn} = 0

        I_{syn} += S_{in}(t) \cdot w_{in}

        \\tau_{syn} \dot{V}_{mem} + V_{mem} = I_{syn} + I_{in}(t) \cdot w_{in} + b + \sigma\zeta(t)

    where :math:`S_{in}(t)` is a vector containing ``1`` for each input channel that emits a spike at time :math:`t`; :math:`w_{in}` is a :math:`[N_{in} \\times N]` matrix of input weights; :math:`I_{in}(t)` is a vector of input currents injected directly onto the neuron membranes; :math:`b` is a :math:`N` vector of bias currents for each neuron; :math:`\\sigma\\zeta(t)` is a white-noise process with standard deviation :math:`\\sigma` injected independently onto each neuron's membrane; and :math:`\\tau_{mem}` and :math:`\\tau_{syn}` are the membrane and synaptic time constants, respectively.

    :On spiking:

    When the membane potential for neuron :math:`j`, :math:`V_{mem, j}` exceeds the threshold voltage :math:`V_{thr} = 0`, then the neuron emits a spike.

    .. math ::

        V_{mem, j} > V_{thr} \\rightarrow S_{rec,j} = 1

        I_{syn} = I_{syn} + S_{rec} \cdot w_{rec}

        V_{mem, j} = V_{mem, j} - 1

    Neurons threfore share a common resting potential of ``0``, a firing threshold of ``0``, and a subtractive reset of ``-1``. Neurons each have an optional bias current `.bias` (default: ``-1``).

    :Surrogate signals:

    To facilitate gradient-based training, a surrogate :math:`U(t)` is generated from the membrane potentials of each neuron. This is used to provide a weighted output :math:`O(t)`.

    .. math ::

        U_j = \\textrm{sig}(V_j)

        O(t) = U(t) \cdot w_{out}

    Where :math:`w_{out}` is a :math:`[N \\times N_{out}]` matrix of output weights, and :math:`\\textrm{sig}(x) = \\left(1 + \\exp(-x)\\right)^{-1}`.

    :Outputs from evolution:

    As output, this layer returns the weighted surrogate activity of the :math:`N` neurons from the `.evolve` method. After each evolution, the attributes `.spikes_last_evolution`, `.i_rec_last_evolution` and `.v_mem_last_evolution` and `.surrogate_last_evolution` will be `.TimeSeries` objects containing the appropriate time series.
    """

    def __init__(
        self,
        w_in: np.ndarray,
        w_recurrent: np.ndarray,
        w_out: np.ndarray,
        tau_mem: FloatVector,
        tau_syn: FloatVector,
        bias: Optional[FloatVector] = -1.0,
        noise_std: Optional[float] = 0.0,
        dt: Optional[float] = None,
        name: Optional[str] = None,
        rng_key: Optional[int] = None,
    ):
        # - Convert arguments to arrays
        w_in = np.array(w_in)
        w_out = np.array(w_out)

        # - Call superclass constructor
        super().__init__(
            w_recurrent, tau_mem, tau_syn, bias, noise_std, dt, name, rng_key
        )

        # - Set correct information about network size
        self._size_in = w_in.shape[0]
        self._size = w_in.shape[1]
        self._size_out = w_out.shape[1]

        # -- Set properties
        self.w_in = w_in
        self.w_out = w_out

    def evolve(
        self,
        ts_input: Optional[TSEvent] = None,
        duration: Optional[float] = None,
        num_timesteps: Optional[int] = None,
        verbose: Optional[bool] = False,
    ) -> TSContinuous:
        """
        Evolve the state of this layer given an input

        :param Optional[TSEvent] ts_input:      Input time series. Default: `None`, no stimulus is provided
        :param Optional[float] duration:        Simulation/Evolution time, in seconds. If not provided, then `num_timesteps` or the duration of `ts_input` is used to determine evolution time
        :param Optional[int] num_timesteps:     Number of evolution time steps, in units of `.dt`. If not provided, then `duration` or the duration of `ts_input` is used to determine evolution time
        :param Optional[bool]verbose:           Currently no effect, just for conformity

        :return TSContinuous:                   Output time series; the synaptic currents of each neuron
        """

        # - Prepare time base and inputs
        time_base, inps, num_timesteps = self._prepare_input_events(
            ts_input, duration, num_timesteps
        )

        # - Call raw evolution function
        time_start = self.t
        Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts = self._evolve_raw(
            inps, inps * 0.0
        )

        # - Record membrane traces
        self.v_mem_last_evolution = TSContinuous(time_base, onp.array(Vmem_ts))

        # - Record spike raster
        spikes_ids = onp.argwhere(onp.array(spike_raster_ts))
        self.spikes_last_evolution = TSEvent(
            spikes_ids[:, 0] * self.dt + time_start,
            spikes_ids[:, 1],
            t_start=time_start,
            t_stop=self.t,
            name="Spikes " + self.name,
            num_channels=self.size,
        )

        # - Record recurrent inputs
        self.i_rec_last_evolution = TSContinuous(time_base, onp.array(Irec_ts))

        # - Record neuron surrogates
        self.surrogate_last_evolution = TSContinuous(time_base, onp.array(surrogate_ts))

        # - Record synaptic currents
        self.i_syn_last_evolution = TSContinuous(time_base, onp.array(Isyn_ts))

        # - Wrap weighted output as time series
        return TSContinuous(time_base, output_ts)

    @property
    def w_in(self) -> np.ndarray:
        """ (np.ndarray) [M,N] input weights """
        return onp.array(self._w_in)

    @w_in.setter
    def w_in(self, value: np.ndarray):
        assert np.ndim(value) == 2, "`w_in` must be 2D"

        assert value.shape == (
            self._size_in,
            self._size,
        ), "`win` must be [{:d}, {:d}]".format(self._size_in, self._size)

        self._w_in = np.array(value).astype("float32")

    @property
    def w_out(self) -> np.ndarray:
        """ (np.ndarray) [N,O] output weights """
        return onp.array(self._w_out)

    @w_out.setter
    def w_out(self, value: np.ndarray):
        assert np.ndim(value) == 2, "`w_out` must be 2D"

        assert value.shape == (
            self._size,
            self._size_out,
        ), "`w_out` must be [{:d}, {:d}]".format(self._size, self._size_out)

        self._w_out = np.array(value).astype("float32")

    @property
    def output_type(self):
        """ (TSContinuous) Output `.TimeSeries` class: `.TSContinuous` """
        return TSContinuous


class RecLIFCurrentInJax_IO(RecLIFJax_IO):
    """
    Recurrent spiking neuron layer (LIF), weighted current input and weighted surrogate output. Input / output weighting provided.

    `.RecLIFJax` is a basic recurrent spiking neuron layer, implemented with a JAX-backed Euler solver backend. Outputs are surrogates generated by each layer neuron, via a set of output weights. Inputs are provided by weighted current injection to each layer neuron, via a set of input weights. The layer is therefore M inputs -> N neurons -> O outputs.

    This layer can be used to implement gradient-based learning systems, using the JAX-provided automatic differentiation functionality of `jax.grad`.

    :Dynamics:

    The dynamics of the :math:`N` neurons' membrane potential :math:`V_{mem}` and the :math:`N` synaptic currents :math:`I_{syn}` evolve under the system

    .. math::

        \\tau_{syn} \dot{I}_{syn} + I_{syn} = 0

        I_{syn} += S_{in}(t) \cdot w_{in}

        \\tau_{syn} \dot{V}_{mem} + V_{mem} = I_{syn} + I_{in}(t) \cdot w_{in} + b + \sigma\zeta(t)

    where :math:`S_{in}(t)` is a vector containing ``1`` for each input channel that emits a spike at time :math:`t`; :math:`w_{in}` is a :math:`[N_{in} \\times N]` matrix of input weights; :math:`I_{in}(t)` is a vector of input currents injected directly onto the neuron membranes; :math:`b` is a :math:`N` vector of bias currents for each neuron; :math:`\\sigma\\zeta(t)` is a white-noise process with standard deviation :math:`\\sigma` injected independently onto each neuron's membrane; and :math:`\\tau_{mem}` and :math:`\\tau_{syn}` are the membrane and synaptic time constants, respectively.

    :On spiking:

    When the membane potential for neuron :math:`j`, :math:`V_{mem, j}` exceeds the threshold voltage :math:`V_{thr} = 0`, then the neuron emits a spike.

    .. math ::

        V_{mem, j} > V_{thr} \\rightarrow S_{rec,j} = 1

        I_{syn} = I_{syn} + S_{rec} \cdot w_{rec}

        V_{mem, j} = V_{mem, j} - 1

    Neurons therefore share a common resting potential of ``0``, a firing threshold of ``0``, and a subtractive reset of ``-1``. Neurons each have an optional bias current `.bias` (default: ``-1``).

    :Surrogate signals:

    To facilitate gradient-based training, a surrogate :math:`U(t)` is generated from the membrane potentials of each neuron. This is used to provide a weighted output :math:`O(t)`.

    .. math ::

        U_j = \\textrm{sig}(V_j)

        O(t) = U(t) \cdot w_{out}

    Where :math:`w_{out}` is a :math:`[N \\times N_{out}]` matrix of output weights, and :math:`\\textrm{sig}(x) = \\left(1 + \\exp(-x)\\right)^{-1}`.

    :Outputs from evolution:

    As output, this layer returns the weighted surrogate activity of the :math:`N` neurons from the `.evolve` method. After each evolution, the attributes `.spikes_last_evolution`, `.i_rec_last_evolution` and `.v_mem_last_evolution` and `.surrogate_last_evolution` will be `.TimeSeries` objects containing the appropriate time series.
    """

    def evolve(
        self,
        ts_input: Optional[TSContinuous] = None,
        duration: Optional[float] = None,
        num_timesteps: Optional[int] = None,
        verbose: Optional[bool] = False,
    ) -> TSEvent:
        """
        Evolve the state of this layer given an input

        :param Optional[TSContinuous] ts_input: Input time series. Default: `None`, no stimulus is provided
        :param Optional[float] duration:        Simulation/Evolution time, in seconds. If not provided, then `num_timesteps` or the duration of `ts_input` is used to determine evolution time
        :param Optional[int] num_timesteps:     Number of evolution time steps, in units of `.dt`. If not provided, then `duration` or the duration of `ts_input` is used to determine evolution time
        :param Optional[bool] verbose:          Currently no effect, just for conformity

        :return TSEvent:                   Output time series; spiking activity each neuron
        """

        # - Prepare time base and inputs
        time_base, inps, num_timesteps = self._prepare_input(
            ts_input, duration, num_timesteps
        )

        # - Call raw evolution function
        time_start = self.t
        Irec_ts, output_ts, surrogate_ts, spike_raster_ts, Vmem_ts, Isyn_ts = self._evolve_raw(
            inps * 0.0, inps
        )

        # - Record membrane traces
        self.v_mem_last_evolution = TSContinuous(time_base, onp.array(Vmem_ts))

        # - Record spike raster
        spikes_ids = onp.argwhere(onp.array(spike_raster_ts))
        self.spikes_last_evolution = TSEvent(
            spikes_ids[:, 0] * self.dt + time_start,
            spikes_ids[:, 1],
            t_start=time_start,
            t_stop=self.t,
            name="Spikes " + self.name,
            num_channels=self.size,
        )

        # - Record recurrent inputs
        self.i_rec_last_evolution = TSContinuous(time_base, onp.array(Irec_ts))

        # - Record neuron surrogates
        self.surrogate_last_evolution = TSContinuous(time_base, onp.array(surrogate_ts))

        # - Record synaptic currents
        self.i_syn_last_evolution = TSContinuous(time_base, onp.array(Isyn_ts))

        # - Wrap weighted output as time series
        return TSContinuous(time_base, output_ts)

    @property
    def input_type(self):
        """ (TSContinuous) Output `.TimeSeries` class: `.TSContinuous` """
        return TSContinuous
