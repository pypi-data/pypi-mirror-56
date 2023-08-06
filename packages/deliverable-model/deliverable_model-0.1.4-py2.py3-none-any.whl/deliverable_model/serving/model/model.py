import importlib
from pathlib import Path
from typing import Callable, Any

from deliverable_model.serving.model.model_loaders.model_loader_base import (
    ModelLoaderBase,
)
from deliverable_model.serving.model.model_loaders.model_registry import (
    get_model_loader_instance_by_type,
)
from deliverable_model.request import Request
from deliverable_model.response import Response
from dill import load


class Model(object):
    def __init__(
        self,
        model_loader_instance: ModelLoaderBase,
        converter_for_request: Callable[[Request], Any],
        converter_for_response: Callable[[Any], Response],
    ):
        self.model_loader_instance = model_loader_instance

        self.converter_for_request = converter_for_request
        self.converter_for_response = converter_for_response

    @classmethod
    def load(cls, asset_dir: Path, metadata) -> "Model":
        # load custom dependency to trigger auto registry for keras
        cls._load_custom_object_dependency(metadata["custom_object_dependency"])

        model_type = metadata["type"]
        model_loader_instance = get_model_loader_instance_by_type(
            model_type, asset_dir, metadata
        )

        converter_for_request = cls._load_function(
            asset_dir / metadata["converter_for_request"]
        ) if metadata.get("converter_for_request") else lambda x: x  # for more easy to test
        converter_for_response = cls._load_function(
            asset_dir / metadata["converter_for_response"]
        ) if metadata.get("converter_for_response") else lambda x: x  # for more easy to test

        self = cls(model_loader_instance, converter_for_request, converter_for_response)

        return self

    def parse(self, request: Request) -> Response:
        native_request = self.converter_for_request(request)

        native_response = self.model_loader_instance.parse(native_request)

        response = self.converter_for_response(native_response)

        return response

    @classmethod
    def _load_custom_object_dependency(cls, custom_object_dependency):
        for dependency in custom_object_dependency:
            importlib.import_module(dependency)

    @classmethod
    def _load_function(cls, serialized_file: Path) -> Callable:
        with serialized_file.open("rb") as fd:
            return load(fd)
