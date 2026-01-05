import logging
import os

from tqdm import tqdm

from models.media_file import MediaFile
from settings import Settings


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    if not os.path.exists(Settings.OUTPUT_LOCATION):
        logging.info(f"Output directory does not exist, creating it at {Settings.OUTPUT_LOCATION}")
        os.makedirs(Settings.OUTPUT_LOCATION)

    directories = [
        d for d in os.listdir(Settings.INPUT_LOCATION) if os.path.isdir(os.path.join(Settings.INPUT_LOCATION, d))
    ]
    logging.info(f"Found {len(directories)} directories in the input directory")

    for i, directory_name in enumerate(directories):
        input_directory = os.path.join(Settings.INPUT_LOCATION, directory_name)
        logging.info(f"Processing directory {i+1}/{len(directories)}: {input_directory}")

        output_directory = os.path.join(Settings.OUTPUT_LOCATION, directory_name)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        errors_directory = os.path.join(Settings.ERRORS_LOCATION, directory_name)
        if not os.path.exists(errors_directory):
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
                media_file.log_error()
                continue

            media_file.copy()
            media_file.fix_creation_time()
            break

        break
