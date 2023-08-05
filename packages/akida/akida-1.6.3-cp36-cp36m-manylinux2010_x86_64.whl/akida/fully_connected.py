from akida.core import Layer, FullyConnectedParams, LearningType, BackendType
from .parameters_filler import fill_fully_connected_params


class FullyConnected(Layer):
    """
    This is used for most processing purposes, since any neuron in the layer
    can be connected to any input channel.

    Outputs are returned from FullyConnected layers as a list of events, that
    is, as a triplet of x, y and feature values. However, FullyConnected
    models by definition have no intrinsic spatial organization. Thus, all
    output events have x and y values of zero with only the f value being
    meaningful – corresponding to the index of the event-generating neuron.
    Note that each neuron can only generate a single event for each packet of
    inputs processed.
    """

    def __init__(self, name, num_neurons, weights_bits=1,
                 learning_type=LearningType.NoLearning, num_weights=0,
                 num_classes=1, initial_plasticity=1, learning_competition=0,
                 min_plasticity=0.1, plasticity_decay=0.25,
                 activations_enabled=True, threshold_fire=0,
                 threshold_fire_step=1, threshold_fire_bits=1,
                 backend_type=BackendType.Software):
        """
        Create a ``FullyConnected`` layer from a name and parameters.

        :param name: name of the layer
        :param num_neurons: number of neurons (filters)
        :param weights_bits: optional, number of bits used to quantize weights
        :param learning_type: optional, learning type
        :param num_weights: optional, number of connections for each neuron
        :param num_classes: optional, number of classes when running in a
         'labeled mode'
        :param initial_plasticity: optional, defines how easily the weights will
         change when learning occurs
        :param learning_competition: optional, controls competition between
         neurons
        :param min_plasticity: optional, defines the minimum level to which
         plasticity will decay
        :param plasticity_decay: optional, defines the decay of plasticity with
         each learning step
        :param activations_enabled: optional, enable or disable activation
         function
        :param threshold_fire: optional, threshold for neurons to fire or
         generate an event
        :param threshold_fire_step: optional, length of the potential
         quantization intervals
        :param threshold_fire_bits: optional, number of bits used to quantize
         the neuron response
        :param backend_type: type of backend for the layer
        :type name: str
        :type num_neurons: int
        :type weights_bits: int
        :type learning_type: LearningType
        :type num_weights: int
        :type num_classes: int
        :type initial_plasticity: int
        :type learning_competition: float
        :type min_plasticity: float
        :type plasticity_decay: float
        :type activations_enabled: bool
        :type threshold_fire: int
        :type threshold_fire_step: float
        :type threshold_fire_bits: int
        :type backend_type: BackendType

        """
        params = FullyConnectedParams()
        fill_fully_connected_params(params, num_neurons=num_neurons,
                                    weights_bits=weights_bits,
                                    learning_type=learning_type,
                                    num_weights=num_weights,
                                    num_classes=num_classes,
                                    initial_plasticity=initial_plasticity,
                                    learning_competition=learning_competition,
                                    min_plasticity=min_plasticity,
                                    plasticity_decay=plasticity_decay,
                                    activations_enabled=activations_enabled,
                                    threshold_fire=threshold_fire,
                                    threshold_fire_step=threshold_fire_step,
                                    threshold_fire_bits=threshold_fire_bits)

        # Call parent constructor to initialize C++ bindings
        # Note that we invoke directly __init__ instead of using super, as
        # specified in pybind documentation
        Layer.__init__(self, params, name, backend_type)
