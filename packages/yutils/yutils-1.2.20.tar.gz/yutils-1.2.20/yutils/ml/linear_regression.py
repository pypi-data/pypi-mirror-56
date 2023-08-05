#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

import numpy as np
import warnings

from yutils.tools.numpy_tools import to_array, r2c, TWO_D_ARRAY_TYPE
from yutils.ml.ml_base import MLObject
from yutils.ml.regression import Regression


FEATURE_AMOUNT_BORDER = 10000


class NormalEquation(MLObject):
    _INPUT_TYPES = dict(original_training_data=TWO_D_ARRAY_TYPE,
                        training_results=TWO_D_ARRAY_TYPE,
                        verbose=bool)

    REGULARIZATION_LAMBDA = 1

    _NONINVERTABILITY_WARNING_MESSAGE = "Non-invertability Warning:\nThis may be a bad use of the Normal Equation.\n" \
                                        "There are too many features in comparison to training examples:\n" \
                                        "# training examples ({data_len}) <= # features ({features})\n" \
                                        "Delete some features or use regularization."
    _CHANGE_METHODS_WARNING = "There are more than {} features, you should use Linear Regression instead."

    def __init__(self, training_data, training_results, assess_for_warning=True, regularization=True, verbose=True):
        super().__init__(original_training_data=to_array(training_data),
                         training_results=r2c(to_array(training_results)),
                         assess_for_warning=assess_for_warning,
                         regularization=regularization,
                         verbose=verbose)
        self.m = training_results.size

        column_of_ones = np.ones(shape=(training_data.shape[0], 1))
        self.training_data = np.append(column_of_ones, training_data, axis=1)

        self.theta = np.zeros(shape=(self.training_data.shape[1], 1))

        self._check_for_warnings(training_data.shape[1])

    def _check_for_warnings(self, num_of_features):
        if not self.assess_for_warning:
            return

        if num_of_features > FEATURE_AMOUNT_BORDER:
            warnings.warn(self._CHANGE_METHODS_WARNING.format(FEATURE_AMOUNT_BORDER))
        if self.m <= num_of_features:
            warnings.warn(self._NONINVERTABILITY_WARNING_MESSAGE.format(data_len=self.m,
                                                                        features=num_of_features))

    def run(self):
        self.theta = np.linalg.pinv(self.training_data.T @ self.training_data + self._get_regularization_value()) @ self.training_data.T @ self.training_results
        self._verbose_print('Theta:\n' + '\n'.join(map(str, self.theta)))

    def _get_regularization_value(self):
        if not self.regularization:
            return 0

        matrix = np.eye(self.training_data.shape[1])
        matrix[0][0] = 0

        return self.REGULARIZATION_LAMBDA * matrix

    def predict(self, input_data):
        input_data = r2c(np.append([1], input_data))
        return sum(input_data * self.theta)[0]


class LinearRegression(Regression):
    _CHANGE_METHODS_WARNING = "There are less than {} features, you should use the Normal Equation instead."

    def _assess_for_warnings(self):
        if self.assess_for_warning and self.original_training_data.shape[1] < FEATURE_AMOUNT_BORDER:
            warnings.warn(self._CHANGE_METHODS_WARNING.format(FEATURE_AMOUNT_BORDER))

    @classmethod
    def _hypothesis(cls, X, theta):
        return X @ theta

    @classmethod
    def compute_cost(cls, X, y, theta, regularization=True):
        m = y.size
        hypothesis = X @ theta
        cost_vector = (hypothesis - y) ** 2

        if regularization:
            regularization_term = (cls.REGULARIZATION_LAMBDA * sum(theta[1:] ** 2))[0]
        else:
            regularization_term = 0

        j_cost = (sum(cost_vector)[0] + regularization_term) / (2 * m)

        return j_cost
