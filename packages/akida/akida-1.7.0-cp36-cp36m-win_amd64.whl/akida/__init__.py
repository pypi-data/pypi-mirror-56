from .core import (Sparse, Tensor, BackendType, ConvolutionMode,
                   PoolingType, LearningType, LayerType, has_backend)

from .layer import *
from .input_data import InputData
from .fully_connected import FullyConnected
from .convolutional import Convolutional
from .separable_convolutional import SeparableConvolutional
from .input_convolutional import InputConvolutional
from .input_bcspike import InputBCSpike
from .model import Model

Layer.set_variable = set_variable
Layer.get_variable = get_variable
Layer.get_variable_names = get_variable_names
Layer.get_learning_histogram = get_learning_histogram

from .inputs import coords_to_sparse, dense_to_sparse
from .observer import Observer
