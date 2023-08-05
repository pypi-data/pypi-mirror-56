import numpy as np
from .core import Layer, LayerType

class LayerStatistics(object):
    '''
    Container attached to an akida.Model and an akida.Layer that allows to
    retrieve layer statistics:
        (average sparsity, number of operations, number of possible spikes,
         row_sparsity)

    '''
    def __init__(self, model, layer):
        self._layer = layer
        self._model = model
        self._sparsity = 0
        self._spiking_loop = 0
        self._num_spikes = 0
        def compute_stats(layer, source_id, spikes, potentials):
            try:
                self._sparsity += spikes.chip(0, source_id).sparsity
                self._spiking_loop += 1
                self._num_spikes += spikes.nnz
            except Exception as e:
                # We swallow any python exception because otherwise it would
                # crash the calling library
                print("Exception in observer callback: " + str(e))

        self._id = model.register_observer(layer, compute_stats)

    def __del__(self):
        self.model.unregister_observer(self._id)

    @property
    def ops(self):
        """Get number of inference operations per input event

        :return: an int that contains the number of operations per event
        """
        layer_params = self._layer.parameters
        if layer_params.layer_type == LayerType.Convolutional:
            return (layer_params.kernel_width * layer_params.kernel_height *
                    layer_params.num_neurons)
        elif layer_params.layer_type == LayerType.SeparableConvolutional:
            ops_dw = layer_params.kernel_width * layer_params.kernel_height
            # Assume we process every potential increment as an event
            spikes_dw = ops_dw
            ops_pw = spikes_dw * layer_params.num_pointwise_neurons
            return ops_dw + ops_pw
        elif layer_params.layer_type == LayerType.FullyConnected:
            return layer_params.num_neurons
        else:
            raise TypeError("Exception in LayerStatistics: ops property is not "
                            "available for " +
                            str(layer_params.layer_type))

    @property
    def possible_spikes(self):
        """Get possible spikes for the layer.

        :return: an integer that contains possible spike amount
        """
        return np.prod(self._layer.output_dims)

    @property
    def row_sparsity(self):
        """Get kernel row sparsity

        Compute row sparsity for kernel weights.

        :return: a float that contains kernel row sparsity
        """
        row_sparsity = 0.0
        if (self._layer.parameters.layer_type == LayerType.Convolutional or
                self._layer.parameters.layer_type == LayerType.SeparableConvolutional):
            weights = self._layer.get_variable("weights")
            wshape = weights.shape
            if np.prod(wshape) == 0:
                raise ValueError("Exception in LayerStatistics: weights shape "
                                "have null dimension: " + str(wshape))

            # Going through all line blocks
            for f in range(wshape[3]):
                for c in range(wshape[2]):
                    for y in range(wshape[1]):
                        if np.array_equal(weights[:, y, c, f], np.zeros((wshape[0]))):
                            # Counting when line block is full of zero.
                            row_sparsity += 1
            return row_sparsity / (wshape[1] * wshape[2] * wshape[3])
        else:
            raise TypeError("Exception in LayerStatistics: row_sparsity "
                            "property is not available for " +
                            str(self._layer.parameters.layer_type))

    @property
    def sparsity(self):
        """Get average sparsity for the layer.

        :return: a float that contains average sparsity
        """
        return 0 if self._spiking_loop == 0 else (self._sparsity
                                                    / self._spiking_loop)

