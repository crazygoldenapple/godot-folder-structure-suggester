from pathlib import Path
from Model.file_manager_helper import FileManagerHelper
from Model.organizer import Organizer
import argparse

def main():
    args = parse_args()
    if args.suggest_refactor:
        run_suggest_refactor(args.path)
    elif args.apply_refactor:
        run_apply_refactor(args.path)
    else:
        run_daily_organizer(args.path)

def run_daily_organizer(root_path: str):
    organizer = Organizer(root_path)
    categorized_file = organizer.classify_files()

def run_suggest_refactor(root_path: str):
    return

def run_apply_refactor(root_path: str):
    return

def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
        parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
        parser.add_argument("--suggest-refactor", action="store_true", help="Suggest refactoring based on the organization.")
        parser.add_argument("--apply-refactor", action="store_true", help="Apply refactoring based on the organization.")
        return parser.parse_args()

if __name__ == "__main__":
    main()