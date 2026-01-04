# Google Photos - Takeout
Fixing metadata of photos extracted from https://takeout.google.com/ before uploading them to a different cloud provider.

## Setup
1. Install main frameworks [with `asdf`](https://asdf-vm.com/): `asdf install`
2. Install Python dependencies: `poetry install`

## Scanning folders
```bash
poetry run python main.py scan  # optionally with -f <folder_name>
```
will browse files in the input location (see `settings.py`) and output all extensions found for media & metadata files.

## Processing folders
```bash
poetry run python main.py run  # optionally with -f <folder_name>
```
will browse files in the input location, and copy them to the output location with:
* creation/modification time matching json metadata (using `xattr` on MacOS)
* when available, geolocation data matching json metadata (using `exiftool`)
