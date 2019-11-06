from ..base.base_model import BaseModel
from ..base.utils import get_model_file
from ...core import Task, DataType
from tensorflow import keras
import tempfile
from tensorflow.keras.utils import to_categorical


def one_hot_encoding(classes):
    return to_categorical(classes)[:, 1:]  # remove category 0


def one_hot_decoding(labels):
    return labels.argmax(axis=1) + 1


class CellTyper(BaseModel):
    """Classifier of single cells."""
    celltype_names = {
        1: 'CD11b- Monocyte',
        2: 'CD11bhi Monocyte',
        3: 'CD11bmid Monocyte',
        4: 'Erythroblast',
        5: 'HSC',
        6: 'Immature B',
        7: 'Mature CD38lo B',
        8: 'Mature CD38mid B',
        9: 'Mature CD4+ T',
        10: 'Mature CD8+ T',
        11: 'Megakaryocyte',
        12: 'Myelocyte',
        13: 'NK',
        14: 'Naive CD4+ T',
        15: 'Naive CD8+ T',
        16: 'Plasma cell',
        17: 'Plasmacytoid DC',
        18: 'Platelet',
        19: 'Pre-B II',
        20: 'Pre-B I'}

    def __init__(self, filename='celltype_model.h5',
                 origin='https://ibm.box.com/shared/static/5uhttlduaund89tpti4y0ptipr2dcj0h.h5',
                 cache_dir=tempfile.mkdtemp()):
        """Initalize the Model."""
        super(CellTyper, self).__init__(
            Task.CLASSIFICATION, DataType.TABULAR
        )
        self.model_path = get_model_file(filename, origin, cache_dir)
        self.model = keras.models.load_model(self.model_path)

    def predict(self, sample, **kwargs):
        """
        Run the model for inference on a given sample and with the provided
        parameters.

        Args:
            sample (object): an input sample for the model.
            kwargs (dict): list of key-value arguments.

        Returns:
            a prediction for the model on the given sample.
        """
        return self.model.predict(
            sample,
            batch_size=None, verbose=0, steps=None, callbacks=None
        )

    @staticmethod
    def logits_to_celltype(predictions):
        return [
            CellTyper.celltype_names[category] for
            category in one_hot_decoding(predictions)
        ]
