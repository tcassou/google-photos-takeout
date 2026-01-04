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
            for metadata_extension in Settings.METADATA_EXTENSIONS:
                metadata_path = self.input_path + metadata_extension
                if not os.path.exists(metadata_path):
                    continue

                with open(metadata_path, "r") as f:
                    self._metadata = SupplementalMetadata.from_json(json.load(f))
                    break

        return self._metadata

    @property
    def is_image(self) -> bool:
        _, ext = os.path.splitext(self.filename)
        return ext in Settings.IMAGE_EXTENSIONS

    @property
    def is_video(self) -> bool:
        _, ext = os.path.splitext(self.filename)
        return ext in Settings.VIDEO_EXTENSIONS

    @property
    def is_other(self) -> bool:
        _, ext = os.path.splitext(self.filename)
        return ext in Settings.OTHER_EXTENTIONS

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

    def fix_geo_data(self) -> None:
        """Write latitude/longitude (and altitude) from metadata into the output file using exiftool."""
        if self.metadata is None:
            raise ValueError("Cannot write geo: metadata is not available")
        if not self.metadata.has_geo:
            raise ValueError("Cannot write geo: metadata has no lat/lon data")
        if self.is_other:
            raise ValueError("Cannot write geo: only images and videos support GPS metadata")

        args = [
            "exiftool",
            "-overwrite_original",
            f"-GPSPosition={self.metadata.latitude},{self.metadata.longitude}",
        ]
        if self.metadata.altitude != 0.0:
            args.extend(
                [
                    "-GPSAltitude=" + str(abs(self.metadata.altitude)),
                    "-GPSAltitudeRef=" + ("0" if self.metadata.altitude >= 0 else "1"),
                ]
            )
        args.append(self.output_path)

        try:
            subprocess.run(args, check=True, capture_output=True, text=True)
        except FileNotFoundError:
            logging.warning("exiftool not found; install with: brew install exiftool")
            raise
        except subprocess.CalledProcessError as e:
            logging.error(f"exiftool failed for {self.filename}: {e.stderr or e.stdout or str(e)}")
            raise
