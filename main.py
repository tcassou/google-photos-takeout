import argparse
import logging
import os

from enum import Enum

from settings import Settings
from lib.run import run_directories
from lib.scan import scan_directories

logging.basicConfig(level=logging.INFO)


class Command(Enum):
    SCAN = "scan"
    RUN = "run"


def main() -> None:
    parser = argparse.ArgumentParser(description="Process Google Photos takeout directories.")
    parser.add_argument(
        "command",
        type=Command,
        help="Main command to run.",
    )
    parser.add_argument(
        "--folder",
        "-f",
        dest="folder",
        help="If provided, only process the specified folder name under the input location.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="When running the 'run' command, skip any step that modifies files (copies, metadata updates).",
    )
    args = parser.parse_args()

    if not os.path.exists(Settings.OUTPUT_LOCATION) and not args.dry_run:
        logging.info(f"Output directory does not exist, creating it at {Settings.OUTPUT_LOCATION}")
        os.makedirs(Settings.OUTPUT_LOCATION)

    # Determine which directories to process based on optional folder argument
    if args.folder:
        candidate_path = os.path.join(Settings.INPUT_LOCATION, args.folder)
        if not os.path.isdir(candidate_path):
            logging.error(f"Specified folder '{args.folder}' does not exist under input location.")
            return
        directories = [args.folder]
    else:
        directories = [
            d for d in os.listdir(Settings.INPUT_LOCATION) if os.path.isdir(os.path.join(Settings.INPUT_LOCATION, d))
        ]

    logging.info(f"Performing {args.command} on {len(directories)} directories")
    match args.command:
        case Command.RUN:
            run_directories(directories, dry_run=args.dry_run)
        case Command.SCAN:
            scan_directories(directories)
        case _:
            raise ValueError(f"Invalid command: {args.command}")


if __name__ == "__main__":
    main()
