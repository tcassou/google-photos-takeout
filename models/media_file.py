import json
import logging
import os
import platform
import shutil
import subprocess

from models.metadata import SupplementalMetadata
from settings import Settings


class MediaFile:
    def __init__(self, input_directory: str, output_directory: str, errors_directory: str, filename: str):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.errors_directory = errors_directory
        self.filename = filename
        self.input_path = os.path.join(self.input_directory, self.filename)
        self.output_path = os.path.join(self.output_directory, self.filename)
        self.errors_path = os.path.join(self.errors_directory, self.filename)
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

    def log_error(self) -> None:
        shutil.copy(self.input_path, self.errors_path)

    def fix_creation_time(self) -> None:
        """Set the file's creation, modification, and access times to the photo taken time from metadata."""
        if self.metadata is None:
            raise ValueError("Cannot fix creation time: metadata is not available")

        # Set modification and access times using os.utime (works on all platforms)
        photo_taken_timestamp = self.metadata.photo_taken_time.timestamp()
        os.utime(self.output_path, (photo_taken_timestamp, photo_taken_timestamp))

        # On macOS, also set the creation time (birthtime) using xattr
        if platform.system() == "Darwin":
            try:
                subprocess.run(
                    [
                        "xattr",
                        "-w",
                        "com.apple.metadata:kMDItemFSCreationDate",
                        self.metadata.photo_taken_time.strftime("%Y-%m-%d %H:%M:%S +0000"),
                        self.output_path,
                    ],
                    check=True,
                    capture_output=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                logging.debug(f"xattr not available for {self.filename}, using modification time only")
