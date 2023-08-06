from akida.core import Layer, FullyConnectedParams, LearningType, BackendType
from .parameters_filler import fill_fully_connected_params


class FullyConnected(Layer):
    """This is used for most processing purposes, since any neuron in the layer
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
                 threshold_fire_step=1, threshold_fire_bits=1):
        """Create a ``FullyConnected`` layer from a name and parameters.

        Args:
            name (str): name of the layer.
            num_neurons (int): number of neurons (filters).
            weights_bits (int, optional): number of bits used to quantize weights.
            learning_type (:obj:`LearningType`, optional): learning type.
            num_weights (int, optional): number of connections for each neuron.
            num_classes (int, optional): number of classes when running in a
                'labeled mode'.
            initial_plasticity (int, optional): defines how easily the weights
                will change when learning occurs.
            learning_competition (float, optional): controls competition between
                neurons.
            min_plasticity (float, optional): defines the minimum level to which
                plasticity will decay.
            plasticity_decay (float, optional): defines the decay of plasticity
                with each learning step.
            activations_enabled (bool, optional): enable or disable activation
                function.
            threshold_fire (int, optional): threshold for neurons to fire or
                generate an event.
            threshold_fire_step (float, optional): length of the potential
                quantization intervals.
            threshold_fire_bits (int, optional): number of bits used to quantize
                the neuron response.

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
        Layer.__init__(self, params, name)
