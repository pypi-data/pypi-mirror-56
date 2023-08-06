from pathlib import Path

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)


class TensorFlowSavedModel(ModelLoaderBase):
    name = "tensorflow_saved_model"

    @classmethod
    def load(cls, model_path: Path, metadata):
        from tensorflow.contrib import predictor

        predictor_func = predictor.from_saved_model(str(model_path))

        self = cls(predictor_func)

        return self
