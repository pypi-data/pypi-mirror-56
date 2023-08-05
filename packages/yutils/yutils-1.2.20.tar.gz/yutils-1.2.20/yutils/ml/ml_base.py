#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python37

from yutils.base import InputChecker
from yutils.exceptions import CodeMistake
from yutils.tools.numpy_tools import to_array, r2c


class MLObject(InputChecker):
    def _verbose_print(self, message):
        if self.verbose:
            print(message)

    @staticmethod
    def _make_column_vector(array):
        if len(array.shape) == 1:
            return r2c(array)
        elif array.shape[1] == 1:
            return array
        raise CodeMistake("Array with shape {shape} isn't a 1D array".format(shape=repr(array.shape)))


def create_data_from_text_file(path):
    data = [line.split(',') for line in open(path, 'r').read().splitlines()]
    features = to_array([line[:-1] for line in data], turn_str_items_to_numeric=True)
    results = to_array([line[-1] for line in data], turn_str_items_to_numeric=True)
    return features, results
