class Settings:
    # Input location contains a list of folders, each containing a list of photos and their supplementary metadata
    INPUT_LOCATION = "/Users/thomas/Downloads/raw"
    # Output location will follow the same structure as the input location, with file metadata fixed
    OUTPUT_LOCATION = "/Users/thomas/Downloads/processed"
    # Each file may have a supplemental metadata file with this extension
    METADATA_EXTENSION = ".supplemental-metadata.json"
    # Supported photo extensions
    SUPPORTED_MEDIA_EXTENSIONS = [".jpg", ".jpeg", ".png", ".heic", ".heif", ".mp4", ".mov"]
