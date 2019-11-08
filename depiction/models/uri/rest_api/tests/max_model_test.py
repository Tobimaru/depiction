"""Test MAX model."""
import unittest
from random import choice

from .....core import Task, DataType
from ..max_model import MAXModel


class ConcreteTestModel(MAXModel):

    def __init__(self, uri, task_type, data_type):
        super(ConcreteTestModel, self).__init__(uri, task_type, data_type)

    def predict(self, sample, *, test_kwarg):
        return sample

    def _process_prediction(self, prediction):
        return prediction

    def _predict(self, sample, *args, **kwargs):
        return sample


class MAXModelTestCase(unittest.TestCase):
    """Test MAX model."""

    def test_initialization(self):
        model = ConcreteTestModel(
            uri='http://localhost:5000',
            task_type=choice(list(Task)),
            data_type=choice(list(DataType))
        )
        self.assertTrue(isinstance(model.metadata, dict))
        self.assertEqual(model.metadata_endpoint, 'model/metadata')
        self.assertEqual(model.labels_endpoint, 'model/labels')
        self.assertEqual(model.endpoint, 'model/predict')
