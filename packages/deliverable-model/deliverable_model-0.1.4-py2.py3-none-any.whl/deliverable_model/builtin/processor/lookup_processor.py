import copy
import typing
from pathlib import Path
from typing import Dict

from deliverable_model.processor_base import ProcessorBase
from deliverable_model.request import Request
from deliverable_model.response import Response

if typing.TYPE_CHECKING:
    from seq2annotation.input import Lookuper


class LookupProcessor(ProcessorBase):
    def __init__(self, padding_parameter=None, lookup_table_registry=None):
        self.lookup_table_registry = (
            lookup_table_registry if lookup_table_registry is not None else {}
        )  # type: Dict[str, "Lookuper"]

        self.padding_parameter = (
            padding_parameter if padding_parameter is not None else {}
        )  # type: Dict[str, str]

    def get_config(self):
        return {
            "lookup_table": list(self.lookup_table_registry.keys()),
            "padding_parameter": self.padding_parameter,
        }

    @classmethod
    def load(cls, parameter: dict, asset_dir) -> "ProcessorBase":
        from seq2annotation.input import Lookuper

        lookup_table_registry = {}

        for instance_name in parameter["lookup_table"]:
            instance_asset = asset_dir / instance_name
            lookup_table_instance = Lookuper.load_from_file(instance_asset)

            lookup_table_registry[instance_name] = lookup_table_instance

        init_parameter = copy.deepcopy(parameter)
        init_parameter.pop("lookup_table")
        init_parameter["lookup_table_registry"] = lookup_table_registry

        self = cls(**init_parameter)

        return self

    def add_vocabulary_lookup_table(self, lookup_table_object: "Lookuper"):
        self._add_lookup_table(lookup_table_object, "vocabulary")

    def add_tag_lookup_table(self, lookup_table_object: "Lookuper"):
        self._add_lookup_table(lookup_table_object, "tag")

    def add_padding_parameter(self, **kwargs):
        self.padding_parameter = kwargs

    def _add_lookup_table(self, lookup_table_object: "Lookuper", name):
        self.lookup_table_registry[name] = lookup_table_object

    def preprocess(self, request: Request) -> Request:
        vocabulary_lookup_table = self.lookup_table_registry["vocabulary"]

        query_id_list = []
        for query_item in request.query:
            query_item_id = [vocabulary_lookup_table.lookup(i) for i in query_item]
            query_id_list.append(query_item_id)

        request.update_query(query_id_list)

        return request

    def postprocess(self, response: Response) -> Response:
        tag_lookup_table = self.lookup_table_registry["tag"]

        data_str_list = []
        for data_int in response.data:
            data_str = [tag_lookup_table.inverse_lookup(i) for i in data_int]
            data_str_list.append(data_str)

        response.update_data(data_str_list)

        return response

    def serialize(self, asset_dir: Path):
        for instance_name, obj in self.lookup_table_registry.items():
            instance_asset = asset_dir / instance_name
            obj.dump_to_file(instance_asset)

    def get_dependency(self) -> list:
        return ["seq2annotation"]
