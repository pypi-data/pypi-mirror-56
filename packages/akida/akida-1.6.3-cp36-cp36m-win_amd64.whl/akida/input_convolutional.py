from akida.core import (Layer, InputConvolutionalParams,
                        ConvolutionMode, PoolingType, BackendType)
from .parameters_filler import fill_input_conv_params

class InputConvolutional(Layer):
    """
    The ``InputConvolutional`` layer is an image-specific input layer.

    It is used if images are sent directly to AEE without using the
    event-generating method. If the User applies their own event-generating
    method, the resulting events should be sent to an InputData type layer
    instead.

    The InputConvolutional layer accepts images in 8-bit pixels, either
    grayscale or RGB. Images are converted to events using a combination of
    convolution kernels, activation thresholds and winner-take-all (WTA)
    policies. Note that since the layer input is dense, expect approximately one
    event per pixel – fewer if there are large contrast-free regions in the
    image, such as with the MNIST dataset.

    Note that this format is not appropriate for neuromorphic camera type input
    which data is natively event-based and should be sent to an InputData type
    input layer.
    """

    def __init__(self, name, input_width, input_height, input_channels,
                 kernel_width, kernel_height, num_neurons,
                 convolution_mode=ConvolutionMode.Same, stride_x=1, stride_y=1,
                 weights_bits=1, pooling_width=-1, pooling_height=-1,
                 pooling_type=PoolingType.NoPooling, pooling_stride_x=-1,
                 pooling_stride_y=-1, activations_enabled=True,
                 threshold_fire=0, threshold_fire_step=1, threshold_fire_bits=1,
                 padding_value=0, backend_type=BackendType.Software):
        """
        Create an ``InputConvolutional`` layer from a name and parameters

        :param name: name of the layer
        :param input_width: input width
        :param input_height: input height
        :param input_channels: number of channels of the input image
        :param kernel_width: convolutional kernel width
        :param kernel_height: convolutional kernel height
        :param num_neurons: number of neurons (filters)
        :param convolution_mode: optional, type of convolution
        :param stride_x: optional, convolution stride X
        :param stride_y: optional, convolution stride Y
        :param weights_bits: optional, number of bits used to quantize weights
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
        :param padding_value: optional, value used when padding
        :param backend_type: type of backend for the layer
        :type name: str
        :type input_width: int
        :type input_height: int
        :type input_channels: int
        :type kernel_width: int
        :type kernel_height: int
        :type num_neurons: int
        :type convolution_mode: ConvolutionMode
        :type stride_x: int
        :type stride_y: int
        :type weights_bits: int
        :type pooling_width: int
        :type pooling_height: int
        :type pooling_type: PoolingType
        :type pooling_stride_x: int
        :type pooling_stride_y: int
        :type activations_enabled: bool
        :type threshold_fire: int
        :type threshold_fire_step: float
        :type threshold_fire_bits: int
        :type padding_value: int
        :type backend_type: BackendType

        """
        params = InputConvolutionalParams()
        fill_input_conv_params(params, input_width=input_width,
                               input_height=input_height,
                               input_channels=input_channels,
                               kernel_width=kernel_width,
                               kernel_height=kernel_height,
                               num_neurons=num_neurons,
                               convolution_mode=convolution_mode,
                               stride_x=stride_x,
                               stride_y=stride_y,
                               weights_bits=weights_bits,
                               pooling_width=pooling_width,
                               pooling_height=pooling_height,
                               pooling_type=pooling_type,
                               pooling_stride_x=pooling_stride_x,
                               pooling_stride_y=pooling_stride_y,
                               activations_enabled=activations_enabled,
                               threshold_fire=threshold_fire,
                               threshold_fire_step=threshold_fire_step,
                               threshold_fire_bits=threshold_fire_bits,
                               padding_value=padding_value)

        # Call parent constructor to initialize C++ bindings
        # Note that we invoke directly __init__ instead of using super, as
        # specified in pybind documentation
        Layer.__init__(self, params, name, backend_type)
