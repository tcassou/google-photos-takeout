import os


class Settings:
    # Input location contains a list of folders, each containing a list of photos and their supplementary metadata
    INPUT_LOCATION = os.path.join(os.path.expandvars("$HOME"), "Downloads", "raw")
    # Output location will follow the same structure as the input location, with file metadata fixed
    OUTPUT_LOCATION = os.path.join(os.path.expandvars("$HOME"), "Downloads", "processed")
    # Errors location will contain files that could not be processed
    ERRORS_LOCATION = os.path.join(os.path.expandvars("$HOME"), "Downloads", "errors")
    # Each file may have a supplemental metadata file with this extension
    METADATA_EXTENSIONS = {
        ".supplemental-metadata.json",
        ".suppl.json",
        ".supplem.json",
        ".suppleme.json",
        ".supplemental.json",
        ".supplemental-.json",
        ".supplemental-m.json",
        ".supplemental-me.json",
        ".supplemental-met.json",
        ".supplemental-metadat.json",
        ".supplemental-metada.json",
    }
    # Supported extensions
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".PNG", ".heic", ".HEIC", ".heif"}
    VIDEO_EXTENSIONS = {".mp4", ".MP4", ".mov", ".MOV"}
    OTHER_EXTENTIONS = {".gif"}
    SUPPORTED_MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | OTHER_EXTENTIONS
