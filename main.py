import logging
import os

from tqdm import tqdm

from models.image import Image
from settings import Settings


logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":

    if not os.path.exists(Settings.OUTPUT_DIRECTORY):
        logging.info(f"Output directory does not exist, creating it at {Settings.OUTPUT_DIRECTORY}")
        os.makedirs(Settings.OUTPUT_DIRECTORY)

    directories = [
        d for d in os.listdir(Settings.INPUT_DIRECTORY) if os.path.isdir(os.path.join(Settings.INPUT_DIRECTORY, d))
    ]
    logging.info(f"Found {len(directories)} directories in the input directory")

    for i, directory in enumerate(directories):
        input_directory_path = os.path.join(Settings.INPUT_DIRECTORY, directory)
        logging.info(f"Processing directory {i+1}/{len(directories)}: {input_directory_path}")

        output_directory_path = os.path.join(Settings.OUTPUT_DIRECTORY, directory)
        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        files = [f for f in os.listdir(input_directory_path) if os.path.isfile(os.path.join(input_directory_path, f))]
        photos = [f for f in files if os.path.splitext(f)[1].lower() in Settings.SUPPORTED_PHOTO_EXTENSIONS]

        progress_bar = tqdm(photos, desc=f"Processing photos in {directory}", leave=True)
        for photo in progress_bar:
            image = Image(os.path.join(input_directory_path, photo))
            progress_bar.set_postfix_str(os.path.basename(image.path))
