import argparse
from ast import parse
from pathlib import Path

from Model.log import Logger

from Model.file_manager_helper import FileManagerHelper as fm
from Model.organizer import Organizer
from Model.time_helper import TimeHelper

logger = Logger(special_prefix="OrganizeProject")

def main():
    args = parse_args()
    if args.daily:
        run_daily_organizer(args.path)
    if args.daily_all:
        run_daily_all_organizer(args.path)

def run_daily_organizer(root_path: str):
    logger.info(f"Running daily organizer on path: {root_path}")
    organizer = Organizer(root_path)
    files_tuple_list = fm.get_files_from_directory(root_path)
    categorized_files, files_to_path = organizer.daily_organize_files(files_tuple_list)
        
    fm.save_file(categorized_files, "FolderStructuringJson", f"{TimeHelper.get_current_date()}_categorized_files.json")
    fm.save_file(files_to_path, "FolderStructuringJson",f"{TimeHelper.get_current_date()}_files_to_path.json")

def run_daily_all_organizer(root_path: str):
    logger.info(f"Running daily all organizer on path: {root_path}")
    organizer = Organizer(root_path)
    files_tuple_list = fm.read_all_directories(root_path)
    categorized_files, files_to_path = organizer.daily_organize_files(files_tuple_list)
        
    fm.save_file(categorized_files, "FolderStructuringJson", f"{TimeHelper.get_current_date()}_categorized_files.json")
    fm.save_file(files_to_path, "FolderStructuringJson",f"{TimeHelper.get_current_date()}_files_to_path.json")

def parse_args() -> argparse.Namespace:
        logger.info("Parsing command line arguments.")
        parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
        parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
        parser.add_argument("--daily", action="store_true", help="Suggest refactoring based on the organization.")
        parser.add_argument("--daily-all", action="store_true", help="Refactor files based on the organization.")
        return parser.parse_args()

if __name__ == "__main__":
    main()