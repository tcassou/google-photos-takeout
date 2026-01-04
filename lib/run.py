import logging
import os

from tqdm import tqdm

from models.media_file import MediaFile
from settings import Settings


def run_directories(directories: list[str], dry_run: bool = False) -> None:
    """
    Run the "run" command, which will:
    - copy media files to the output location
    - fix the creation time of the media files based on the metadata
    - log any errors to the errors location
    """
    if dry_run:
        logging.info("Dry run: no files will be copied or modified")

    for i, directory_name in enumerate(directories):
        input_directory = os.path.join(Settings.INPUT_LOCATION, directory_name)
        logging.info(f"Processing directory {i+1}/{len(directories)}: {input_directory}")

        output_directory = os.path.join(Settings.OUTPUT_LOCATION, directory_name)
        if not os.path.exists(output_directory) and not dry_run:
            os.makedirs(output_directory)

        errors_directory = os.path.join(Settings.ERRORS_LOCATION, directory_name)
        if not os.path.exists(errors_directory) and not dry_run:
            os.makedirs(errors_directory)

        files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
        filenames = [f for f in files if os.path.splitext(f)[1].lower() in Settings.SUPPORTED_MEDIA_EXTENSIONS]

        progress_bar = tqdm(filenames, desc=f"Processing photos in {directory_name}", leave=True)
        for filename in progress_bar:
            media_file = MediaFile(
                input_directory=input_directory,
                output_directory=output_directory,
                errors_directory=errors_directory,
                filename=filename,
            )
            progress_bar.set_postfix_str(media_file.filename)

            if media_file.metadata is None:
                if not dry_run:
                    media_file.log_error()
                continue

            if not dry_run:
                media_file.copy()

                if media_file.is_other:
                    continue
                if media_file.metadata.has_geo:
                    media_file.fix_geo_data()

                media_file.fix_creation_time()
