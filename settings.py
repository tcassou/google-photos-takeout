class Settings:
    # Input directory contains a list of directories, each containing a list of photos and their supplementary metadata
    INPUT_DIRECTORY = "/Users/thomas/Downloads/raw"
    # Output directory will follow the same structure as the input directory, with file metadata fixed
    OUTPUT_DIRECTORY = "/Users/thomas/Downloads/processed"
    # Each file may have a supplemental metadata file with this extension
    METADATA_EXTENSION = ".supplemental-metadata.json"
    # Supported photo extensions
    SUPPORTED_PHOTO_EXTENSIONS = [".jpg", ".jpeg", ".png", ".heic", ".heif"]
