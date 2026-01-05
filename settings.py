class Settings:
    # Input location contains a list of folders, each containing a list of photos and their supplementary metadata
    INPUT_LOCATION = "/Users/thomas/Downloads/raw"
    # Output location will follow the same structure as the input location, with file metadata fixed
    OUTPUT_LOCATION = "/Users/thomas/Downloads/processed"
    # Errors location will contain files that could not be processed
    ERRORS_LOCATION = "/Users/thomas/Downloads/errors"
    # Each file may have a supplemental metadata file with this extension
    METADATA_EXTENSIONS = [
        ".supplemental-metadata.json",
        ".suppl.json",
    ]
    # Supported extensions
    SUPPORTED_MEDIA_EXTENSIONS = [".jpg", ".jpeg", ".png", ".heic", ".heif", ".mp4", ".mov"]
