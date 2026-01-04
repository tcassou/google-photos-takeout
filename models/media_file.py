import json
import os
import shutil

from models.metadata import SupplementalMetadata
from settings import Settings


class MediaFile:
    def __init__(self, input_directory: str, output_directory: str, filename: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.filename = filename
        self.input_path = os.path.join(self.input_directory, self.filename)
        self.output_path = os.path.join(self.output_directory, self.filename)
        self._metadata = None

    @property
    def metadata(self) -> SupplementalMetadata:
        if self._metadata is None:
            metadata_path = self.input_path + Settings.METADATA_EXTENSION
            if not os.path.exists(metadata_path):
                return None

            with open(metadata_path, "r") as f:
                self._metadata = SupplementalMetadata.from_json(json.load(f))

        return self._metadata

    def copy(self) -> None:
        shutil.copy(self.input_path, self.output_path)

    # def fix_creation_time(self) -> None:
