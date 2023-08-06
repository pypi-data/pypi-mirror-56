import json
from pathlib import Path

from deliverable_model.builder.metadata.metadata_builder import MetadataBuilder
from deliverable_model.builder.model.model_builder import ModelBuilder
from deliverable_model.builder.processor.processor_builder import ProcessorBuilder
from deliverable_model.utils import create_dir_if_needed


class DeliverableModelBuilder(object):
    def __init__(self, export_dir):
        self.export_dir = Path(export_dir)

        self.processor_builder = None  # type: ProcessorBuilder
        self.model_builder = None  # type: ModelBuilder
        self.metadata_builder = None  # type: MetadataBuilder

    def add_metadata(self, metadata_builder: MetadataBuilder):
        self.metadata_builder = metadata_builder

    def add_processor(self, processor_builder: ProcessorBuilder):
        self.processor_builder = processor_builder

    def add_model(self, model_builder: ModelBuilder):
        self.model_builder = model_builder

    def save(self):
        dependency = self.gather_dependency()

        export_data = {
            "version": "1.0",
            "dependency": dependency,
            "processor": self.processor_builder.serialize(
                create_dir_if_needed(self.export_dir / "asset" / "processor")
            ),
            "model": self.model_builder.serialize(
                create_dir_if_needed(self.export_dir / "asset" / "model")
            ),
            "metadata": self.metadata_builder.serialize(
                create_dir_if_needed(self.export_dir / "asset" / "metadata")
            ),
        }

        metadata_file = self.export_dir / "metadata.json"

        with metadata_file.open("wt") as fd:
            json.dump(export_data, fd)

        return export_data

    def gather_dependency(self) -> list:
        dependency = []

        dependency.extend(self.metadata_builder.get_dependency())
        dependency.extend(self.model_builder.get_dependency())
        dependency.extend(self.processor_builder.get_dependency())

        return list(sorted(set(dependency)))
