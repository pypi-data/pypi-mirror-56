import shutil
from collections import namedtuple
from pathlib import Path
import typing
from typing import List, Any, Callable

from deliverable_model.request import Request
from dill import dump

if typing.TYPE_CHECKING:
    from deliverable_model.response import Response

ModelInfo = namedtuple("ModelInfo", ["type", "store_dir"])


def simple_converter_for_request(request: Request) -> Any:
    return request.query


def simple_converter_for_response(response: Any) -> "Response":
    from deliverable_model.response import Response

    return Response(response)


class ModelBuilder(object):
    version = "1.0"

    def __init__(self):
        self.model = None  # type: ModelInfo
        self.dependency = ["tensorflow"]
        self.custom_object_dependency = []

        self.converter_for_request = (
            simple_converter_for_request
        )  # type: Callable[[Request], Any]
        self.converter_for_response = (
            simple_converter_for_response
        )  # type: Callable[[Any], Response]

    def add_keras_h5_model(self, model_dir):
        if self.model:
            raise ValueError()

        self.model = ModelInfo("keras_h5_model", model_dir)

    def add_tensorflow_saved_model(self, model_dir):
        if self.model:
            raise ValueError()

        self.model = ModelInfo("tensorflow_saved_model", model_dir)

    def add_keras_saved_model(self, model_dir):
        if self.model:
            raise ValueError()

        self.model = ModelInfo("keras_saved_model", model_dir)

    def add_dummy_model(self, model_dir):
        if self.model:
            raise ValueError()

        self.model = ModelInfo("dummy_model", model_dir)

    def add_converter_for_request(self, func: Callable):
        self.converter_for_request = func

    def add_converter_for_response(self, func: Callable):
        self.converter_for_response = func

    @staticmethod
    def _dump_function(
        assert_dir: Path, serialized_file_name: str, func: Callable
    ) -> str:
        serialized_file = assert_dir / serialized_file_name

        with serialized_file.open("wb") as fd:
            dump(func, fd)

        return serialized_file_name

    def save(self):
        self.build = True

    def serialize(self, asset_dir: Path):
        output_dir = asset_dir / self.model.type

        shutil.copytree(self.model.store_dir, output_dir)

        return {
            "version": self.version,
            "type": self.model[0],
            "custom_object_dependency": self.custom_object_dependency,
            "converter_for_request": self._dump_function(
                asset_dir, "converter_for_request", self.converter_for_request
            ),
            "converter_for_response": self._dump_function(
                asset_dir, "converter_for_response", self.converter_for_response
            ),
        }

    def get_dependency(self):
        return self.dependency

    def set_dependency(self, dependency: List[str]):
        self.dependency = dependency

    def append_dependency(self, dependency: List[str]):
        self.dependency = self.dependency + dependency

    def set_custom_object_dependency(self, dependency: List[str]):
        self.custom_object_dependency = dependency
