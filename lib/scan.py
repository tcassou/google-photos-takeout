import logging
import os
from typing import List

from tqdm import tqdm

from settings import Settings


def scan_directories(directories: List[str]) -> None:
    """
    Browse files in the given input folders and output:
    - all extensions found for media files (ex: .png, .jpg)
    - all extensions found for metadata files (ex: .xxx.json, .yyy.json)
    - compare with the extensions defined in Settings and highlight any new extensions found
    """
    media_extensions: set[str] = set()
    metadata_extensions: set[str] = set()

    progress_bar = tqdm(directories, desc="Scanning directories", leave=True)
    for directory_name in progress_bar:
        input_directory = os.path.join(Settings.INPUT_LOCATION, directory_name)
        progress_bar.set_postfix_str(directory_name)

        if not os.path.isdir(input_directory):
            logging.warning(f"Skipping non-directory path: {input_directory}")
            continue

        # Only look at files at the top level of each directory
        files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

        for filename in files:
            basename, ext = os.path.splitext(filename)
            # If it's a JSON file, try to interpret it as a metadata file with the "abc.xxx.json" pattern
            if ext == ".json":
                _, ext_prefix = os.path.splitext(basename)
                if ext_prefix:
                    metadata_extensions.add(ext_prefix + ext)
                continue

            # Anything that is not a JSON file is considered a media file (e.g. ".jpg", ".mp4")
            if ext:
                media_extensions.add(ext)

    new_media_exts = sorted(media_extensions - Settings.SUPPORTED_MEDIA_EXTENSIONS)
    new_metadata_exts = sorted(metadata_extensions - Settings.METADATA_EXTENSIONS)

    if new_media_exts:
        logging.info(f"⚠️ New media extensions not in settings: {new_media_exts}")
    else:
        logging.info("✅ No new media extensions compared to settings.")

    if new_metadata_exts:
        logging.info(f"⚠️ New metadata extensions not in settings: {new_metadata_exts}")
    else:
        logging.info("✅ No new metadata extensions compared to settings.")
