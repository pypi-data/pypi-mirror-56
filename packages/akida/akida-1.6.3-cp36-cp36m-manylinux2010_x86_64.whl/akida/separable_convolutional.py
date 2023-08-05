from akida.core import (Layer, SeparableConvolutionalParams, LearningType,
                        ConvolutionMode, PoolingType, BackendType)
from .parameters_filler import fill_separable_conv_params

class SeparableConvolutional(Layer):
    """
    Separable convolutions consist in first performing a depthwise spatial
    convolution (which acts on each input channel separately) followed by a
    pointwise convolution which mixes together the resulting output channels.
    Intuitively, separable convolutions can be understood as a way to factorize
    a convolution kernel into two smaller kernels, thus decreasing the number of
    computations required to evaluate the output potentials. The
    ``SeparableConvolutional`` layer can also integrate a final pooling
    operation to reduce its spatial output dimensions.
    """

    def __init__(self, name, kernel_width, kernel_height, num_neurons,
                 num_pointwise_neurons, convolution_mode=ConvolutionMode.Same,
                 weights_bits=2, learning_type=LearningType.NoLearning,
                 num_weights=0, num_classes=1, initial_plasticity=1,
                 learning_competition=0, min_plasticity=0.1,
                 plasticity_decay=0.25, pooling_width=-1, pooling_height=-1,
                 pooling_type=PoolingType.NoPooling, pooling_stride_x=-1,
                 pooling_stride_y=-1, activations_enabled=True,
                 threshold_fire=0, threshold_fire_step=1,
                 threshold_fire_bits=1, backend_type=BackendType.Software):
        """
        Create a ``SeparableConvolutional`` layer from a name and
        parameters.

        :param name: name of the layer
        :param kernel_width: convolutional kernel width
        :param kernel_height: convolutional kernel height
        :param num_neurons: number of neurons (filters)
        :param num_pointwise_neurons: number of pointwise neurons
        :param convolution_mode: optional, type of convolution
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
        :param pooling_width: optional, pooling window width. If set to -1 it
         will be global
        :param pooling_height: optional, pooling window height. If set to -1 it
         will be global
        :param pooling_type: optional, pooling type (None, Max or Average)
        :param pooling_stride_x: optional, pooling stride on x dimension
        :param pooling_stride_y: optional, pooling stride on y dimension
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
        :type kernel_width: int
        :type kernel_height: int
        :type num_neurons: int
        :type num_pointwise_neurons: int
        :type convolution_mode: ConvolutionMode
        :type weights_bits: int
        :type learning_type: LearningType
        :type num_weights: int
        :type num_classes: int
        :type initial_plasticity: int
        :type learning_competition: float
        :type min_plasticity: float
        :type plasticity_decay: float
        :type pooling_width: int
        :type pooling_height: int
        :type pooling_type: PoolingType
        :type pooling_stride_x: int
        :type pooling_stride_y: int
        :type activations_enabled: bool
        :type threshold_fire: int
        :type threshold_fire_step: float
        :type threshold_fire_bits: int
        :type backend_type: BackendType
        """
        params = SeparableConvolutionalParams()
        fill_separable_conv_params(params, kernel_width=kernel_width,
                                   kernel_height=kernel_height,
                                   num_neurons=num_neurons,
                                   num_pointwise_neurons=num_pointwise_neurons,
                                   convolution_mode=convolution_mode,
                                   weights_bits=weights_bits,
                                   learning_type=learning_type,
                                   num_weights=num_weights,
                                   num_classes=num_classes,
                                   initial_plasticity=initial_plasticity,
                                   learning_competition=learning_competition,
                                   min_plasticity=min_plasticity,
                                   plasticity_decay=plasticity_decay,
                                   pooling_width=pooling_width,
                                   pooling_height=pooling_height,
                                   pooling_type=pooling_type,
                                   pooling_stride_x=pooling_stride_x,
                                   pooling_stride_y=pooling_stride_y,
                                   activations_enabled=activations_enabled,
                                   threshold_fire=threshold_fire,
                                   threshold_fire_step=threshold_fire_step,
                                   threshold_fire_bits=threshold_fire_bits)

        # Call parent constructor to initialize C++ bindings
        # Note that we invoke directly __init__ instead of using super, as
        # specified in pybind documentation
        Layer.__init__(self, params, name, backend_type)
