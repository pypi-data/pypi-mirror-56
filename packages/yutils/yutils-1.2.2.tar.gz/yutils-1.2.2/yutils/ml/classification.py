#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

import numpy as np
import scipy.optimize as spopt

from yutils.tools.numpy_tools import to_array, r2c
from yutils.ml.ml_base import MLObject
from yutils.ml.regression import Regression


class LogisticRegressionClassifier(Regression):
    @classmethod
    def _hypothesis(cls, X, theta):
        return cls._sigmoid(X @ theta)

    @staticmethod
    def _sigmoid(z):
        return 1 / (1 + np.exp(-z))

    @classmethod
    def compute_cost(cls, X, y, theta, regularization=True):
        theta = cls._make_column_vector(theta)
        m = y.size

        y_true_computation = (y.T @ np.log(cls._hypothesis(X, theta)))[0][0]
        y_false_computation = ((1 - y).T @ np.log(1 - cls._hypothesis(X, theta)))[0][0]

        if regularization:
            regularization_term = (cls.REGULARIZATION_LAMBDA / (2 * m)) * sum(theta[1:] ** 2)[0]
        else:
            regularization_term = 0

        j_cost_no_reg = ((1 / m) * (-y_true_computation - y_false_computation))
        j_cost = j_cost_no_reg + regularization_term
        return j_cost

    def check_prediction(self):
        training_data_prediction = self._hypothesis(self.training_data, self.theta) >= 0.5
        correspondence = training_data_prediction == self.training_results[:, 0]
        return np.count_nonzero(correspondence) / correspondence.size


class LogisticRegressionOptimizedClassifier(LogisticRegressionClassifier):
    def run(self):
        self._initialize_all_data()

        result = spopt.minimize(self._get_cost_and_gradient,
                                self.theta,
                                jac=True,
                                options=dict(maxiter=self.iterations, disp=self.verbose))

        if not result.success:
            raise Exception(result.message)

        self.theta = result.x

    def _get_cost_and_gradient(self, theta):
        return self.compute_cost(self.training_data, self.training_results, theta, self.regularization), \
               self.get_gradient(self.training_data, self.training_results, theta, self.regularization)[:, 0]


class MultiClassClassification(MLObject):
    def __init__(self, training_data, training_results, learning_rate=Regression.DEFAULT_LEARNING_RATE,
                 iterations=Regression.DEFAULT_ITERATIONS, normalization=True, verbose=True):
        super().__init__(training_data=to_array(training_data),
                         training_results=r2c(to_array(training_results)),
                         learning_rate=learning_rate,
                         iterations=iterations,
                         normalization=normalization,
                         verbose=verbose)
        self.input_kwargs = dict(learning_rate=learning_rate,
                                 iterations=iterations,
                                 normalization=normalization,
                                 verbose=verbose)
        self.logistic_regression_classes = []

    def run(self):
        for result_class in np.unique(self.training_results):
            training_results = np.where(self.training_results == result_class, 1, 0)
            log_reg_obj = LogisticRegressionOptimizedClassifier(self.training_data, training_results, **self.input_kwargs)
            log_reg_obj.run()
            self.logistic_regression_classes.append(log_reg_obj)

    def predict(self, input_data):
        # TODO: when predict classes give a probability and not a boolean,
        #  change this to find the class with max probability
        for i, obj in enumerate(self.logistic_regression_classes):
            if obj.predict(input_data) > 0.5:
                print('Class', i + 1)
