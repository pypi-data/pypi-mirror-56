import akida.core as ak


def serialize_learning_type(learning_type):
    if learning_type == ak.LearningType.NoLearning:
        return "none"
    if learning_type == ak.LearningType.AkidaUnsupervised:
        return "akidaUnsupervised"


def serialize_convolution_mode(convolution_mode):
    if convolution_mode == ak.ConvolutionMode.Valid:
        return "valid"
    if convolution_mode == ak.ConvolutionMode.Same:
        return "same"
    if convolution_mode == ak.ConvolutionMode.Full:
        return "full"


def serialize_pooling_type(pooling_type):
    if pooling_type == ak.PoolingType.NoPooling:
        return "none"
    if pooling_type == ak.PoolingType.Max:
        return "max"
    if pooling_type == ak.PoolingType.Average:
        return "average"


def serialize_num_neurons_params(params, params_dict):
    params_dict["numNeurons"] = params.num_neurons


def serialize_weights_bits_params(params, params_dict):
    params_dict["weightsBits"] = params.weights_bits


def serialize_learning_params(params, params_dict):
    params_dict["learningType"] = serialize_learning_type(params.learning_type)
    params_dict["numWeights"] = params.num_weights
    params_dict["numClasses"] = params.num_classes
    params_dict["initialPlasticity"] = params.initial_plasticity
    params_dict["learningCompetition"] = params.learning_competition
    params_dict["minPlasticity"] = params.min_plasticity
    params_dict["plasticityDecay"] = params.plasticity_decay


def serialize_activations_params(params, params_dict):
    if not params.activations_params.activations_enabled:
        params_dict["activations"] = "none"
    params_dict["thresholdFire"] = params.activations_params.threshold_fire
    params_dict["thresholdFireStep"] = params.activations_params.threshold_fire_step
    params_dict["thresholdFireBits"] = params.activations_params.threshold_fire_bits


def serialize_convolution_kernel_params(params, params_dict):
    params_dict["kernelWidth"] = params.kernel_width
    params_dict["kernelHeight"] = params.kernel_height
    params_dict["convolutionMode"] = serialize_convolution_mode(
        params.convolution_mode)


def serialize_input_params(params, params_dict):
    params_dict["inputWidth"] = params.input_width
    params_dict["inputHeight"] = params.input_height


def serialize_pooling_params(params, params_dict):
    params_dict["poolingWidth"] = params.pooling_width
    params_dict["poolingHeight"] = params.pooling_height
    params_dict["poolingType"] = serialize_pooling_type(params.pooling_type)
    params_dict["poolStrideX"] = params.pooling_stride_x
    params_dict["poolStrideY"] = params.pooling_stride_y


def serialize_input_data_params(params, params_dict):
    serialize_input_params(params, params_dict)
    params_dict["inputFeatures"] = params.input_features
    params_dict["packetSize"] = params.packet_size
    params_dict["accumulate"] = "true" if params.accumulate else "false"


def serialize_stride_params(params, params_dict):
    params_dict["strideX"] = params.stride_x
    params_dict["strideY"] = params.stride_y


def serialize_data_processing_params(params, params_dict):
    serialize_num_neurons_params(params, params_dict)
    serialize_weights_bits_params(params, params_dict)
    serialize_learning_params(params, params_dict)
    serialize_activations_params(params, params_dict)


def serialize_fully_connected_params(params, params_dict):
    serialize_data_processing_params(params, params_dict)


def serialize_conv_params(params, params_dict):
    serialize_data_processing_params(params, params_dict)
    serialize_convolution_kernel_params(params, params_dict)
    serialize_pooling_params(params, params_dict)


def serialize_separable_conv_params(params, params_dict):
    serialize_conv_params(params, params_dict)
    params_dict["numPointwiseNeurons"] = params.num_pointwise_neurons


def serialize_input_conv_params(params, params_dict):
    serialize_input_params(params, params_dict)
    serialize_convolution_kernel_params(params, params_dict)
    serialize_stride_params(params, params_dict)
    serialize_num_neurons_params(params, params_dict)
    serialize_weights_bits_params(params, params_dict)
    serialize_pooling_params(params, params_dict)
    serialize_activations_params(params, params_dict)
    params_dict["inputChannels"] = params.input_channels
    params_dict["paddingValue"] = params.padding_value


def serialize_parameters(params):
    params_dict = {}

    if params.layer_type == ak.LayerType.InputData:
        params_dict["layerType"] = "inputData"
        serialize_input_data_params(params, params_dict)
    if params.layer_type == ak.LayerType.InputConvolutional:
        params_dict["layerType"] = "inputConvolutional"
        serialize_input_conv_params(params, params_dict)
    if params.layer_type == ak.LayerType.FullyConnected:
        params_dict["layerType"] = "fullyConnected"
        serialize_fully_connected_params(params, params_dict)
    if params.layer_type == ak.LayerType.Convolutional:
        params_dict["layerType"] = "convolutional"
        serialize_conv_params(params, params_dict)
    if params.layer_type == ak.LayerType.SeparableConvolutional:
        params_dict["layerType"] = "separableConvolutional"
        serialize_separable_conv_params(params, params_dict)

    return params_dict

def deserialize_parameters(params):
    type = str()
    params_dict = {}
    for item in params:
        if item == "layerType":
            type = str(params[item])
        elif item == "inputWidth":
            params_dict["input_width"] = params[item]
        elif item == "inputHeight":
            params_dict["input_height"] = params[item]
        elif item == "convolutionMode":
            if params[item] == "valid":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Valid
            elif params[item] == "same":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Same
            elif params[item] == "full":
                params_dict["convolution_mode"] = ak.ConvolutionMode.Full
            else:
                raise ValueError("'convolutionMode' should be 'valid', "
                                 "'same' or 'full'")
        elif item == "kernelWidth":
            params_dict["kernel_width"] = params[item]
        elif item == "kernelHeight":
            params_dict["kernel_height"] = params[item]
        elif item == "kernelSize":
            params_dict["kernel_width"] = params[item]
            params_dict["kernel_height"] = params[item]
        elif item == "strideX":
            params_dict["stride_x"] = params[item]
        elif item == "strideY":
            params_dict["stride_y"] = params[item]
        elif item == "stride":
            params_dict["stride_x"] = params[item]
            params_dict["stride_y"] = params[item]
        elif item == "poolingWidth":
            params_dict["pooling_width"] = params[item]
        elif item == "poolingHeight":
            params_dict["pooling_height"] = params[item]
        elif item == "poolingSize":
            params_dict["pooling_width"] = params[item]
            params_dict["pooling_height"] = params[item]
        elif item == "poolingType":
            if params[item] == "none":
                params_dict["pooling_type"] = ak.PoolingType.NoPooling
            elif params[item] == "max":
                params_dict["pooling_type"] = ak.PoolingType.Max
            elif params[item] == "average":
                params_dict["pooling_type"] = ak.PoolingType.Average
            else:
                raise ValueError("'poolingType' should be 'none', 'max' "
                                 "or 'average'")
        elif item == "poolStrideX":
            params_dict["pooling_stride_x"] = params[item]
        elif item == "poolStrideY":
            params_dict["pooling_stride_y"] = params[item]
        elif item == "numNeurons":
            params_dict["num_neurons"] = params[item]
        elif item == "weightsBits":
            params_dict["weights_bits"] = params[item]
        elif item == "learningType":
            if params[item] == "none":
                params_dict["learning_type"] = ak.LearningType.NoLearning
            elif params[item] == "akidaUnsupervised":
                params_dict["learning_type"] = ak.LearningType.AkidaUnsupervised
            else:
                raise ValueError("'learningType' should be 'none' or 'akidaUnsupervised'")
        elif item == "numWeights":
            params_dict["num_weights"] = params[item]
        elif item == "numClasses":
            params_dict["num_classes"] = params[item]
        elif item == "initialPlasticity":
            params_dict["initial_plasticity"] = params[item]
        elif item == "learningCompetition":
            params_dict["learning_competition"] = params[item]
        elif item == "minPlasticity":
            params_dict["min_plasticity"] = params[item]
        elif item == "plasticityDecay":
            params_dict["plasticity_decay"] = params[item]
        elif item == "activations":
            if params[item] == "none":
                params_dict["activations_enabled"] = False
            elif params[item] == "true":
                pass # activations are enabled by default
            else:
                raise ValueError("'activations' should be 'none' or 'true'")
        elif item == "thresholdFire":
            params_dict["threshold_fire"] = params[item]
        elif item == "thresholdFireStep":
            params_dict["threshold_fire_step"] = params[item]
        elif item == "thresholdFireBits":
            params_dict["threshold_fire_bits"] = params[item]
        elif item == "inputChannels":
            params_dict["input_channels"] = params[item]
        elif item == "paddingValue":
            params_dict["padding_value"] = params[item]
        elif item == "inputFeatures":
            params_dict["input_features"] = params[item]
        elif item == "packetSize":
            params_dict["packet_size"] = params[item]
        elif item == "accumulate":
            if params[item] == "true":
                params_dict["accumulate"] = True
            elif params[item] == "false":
                params_dict["accumulate"] = False
            else:
                raise ValueError("'accumulate' should be 'true' or 'false'")
        elif item == "numPointwiseNeurons":
            params_dict["num_pointwise_neurons"] = params[item]
        else:
            raise ValueError("Unknown parameter: " +
                             item + ": " + str(params[item]))
    return type, params_dict
