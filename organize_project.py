import argparse
from pathlib import Path

from Model.log import Logger

from Model.file_manager_helper import FileManagerHelper
from Model.organizer import Organizer
from Model.time_helper import TimeHelper

logger = Logger(special_prefix="OrganizeProject")

def main():
    args = parse_args()
    if args.daily:
        run_daily_organizer(args.path)

def run_daily_organizer(root_path: str):
    logger.info(f"Running daily organizer on path: {root_path}")
    organizer = Organizer(root_path)
    categorized_files, files_to_path = organizer.daily_organize_files()
        
    FileManagerHelper.save_file(categorized_files, "FolderStructuringJson", f"{TimeHelper.get_current_date()}_categorized_files.json")
    FileManagerHelper.save_file(files_to_path, "FolderStructuringJson",f"{TimeHelper.get_current_date()}_files_to_path.json")

def parse_args() -> argparse.Namespace:
        logger.info("Parsing command line arguments.")
        parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
        parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
        parser.add_argument("--daily", action="store_true", help="Suggest refactoring based on the organization.")
        return parser.parse_args()

if __name__ == "__main__":
    main()