import numpy as np

from akida.core import Layer, Tensor
from .layer_statistics import LayerStatistics

def set_variable(self, name, values):
    """Set the value of a layer variable.

    Layer variables are named entities representing the weights or
    thresholds used during inference:

    * Weights variables are typically integer arrays of shape:
        (num_neurons, features/channels, height, width) col-major ordered ('F')
        or equivalently:
        (width, height, features/channels, num_neurons) row-major ('C')
    * Threshold variables are typically integer or float arrays of shape:
        (num_neurons)

    :param name: the variable name
    :type name: str
    :param values: a numpy.ndarray containing the variable values
    :type values: numpy.ndarray
    """
    if values.flags['C_CONTIGUOUS']:
        tensor = Tensor(values)
    else:
        tensor = Tensor(np.ascontiguousarray(values))
    self.variables.set(name, tensor)

def get_variable(self, name):
    """Get the value of a layer variable.

    Layer variables are named entities representing the weights or
    thresholds used during inference:

    * Weights variables are typically integer arrays of shape:
        (width, height, features/channels, num_neurons) row-major ('C')
    * Threshold variables are typically integer or float arrays of shape:
        (num_neurons)

    :param name: the variable name
    :type name: str
    :return: a numpy.ndarray containing the variable
    """
    return self.variables.get(name).to_numpy()

def get_variable_names(self):
    """Get the list of variable names for this layer.

    :return: a list of variable names
    """
    return self.variables.names

def get_learning_histogram(self):
    """Returns an histogram of learning percentages.

    Returns a list of learning percentages and the associated number of
    neurons.

    :return: a (n,2) numpy.ndarray containing the learning percentages and
     the number of neurons
    """
    histogram = np.zeros((100,2), dtype=np.uint32)
    num_neurons = self.get_variable("weights").shape[3]
    num_weights = np.count_nonzero(self.get_variable("weights")) / num_neurons
    for i in range(num_neurons):
        threshold_learn = self.get_variable("threshold_learning")[i]
        learn_percentage = int(100 * threshold_learn / num_weights)
        histogram[learn_percentage, 0] = learn_percentage
        histogram[learn_percentage, 1] += 1
    return histogram[histogram[:, 0] != 0, :]
