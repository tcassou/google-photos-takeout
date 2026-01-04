import json
import os

from models.metadata import SupplementalMetadata
from settings import Settings


class Image:
    def __init__(self, path: str):
        self.path = path
        self._metadata = None

    @property
    def metadata(self) -> SupplementalMetadata:
        if self._metadata is None:
            metadata_path = self.path + Settings.METADATA_EXTENSION
            if not os.path.exists(metadata_path):
                return None

            with open(self.path + Settings.METADATA_EXTENSION, "r") as f:
                self._metadata = SupplementalMetadata.from_json(json.load(f))

        return self._metadata
