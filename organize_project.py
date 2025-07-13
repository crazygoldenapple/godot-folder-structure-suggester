from pathlib import Path
from Model.organizer import *
import argparse

def main():
    root_path = parse_args().path
    organizer = Organizer(root_path, Path.cwd())
    categorized_file = organizer.arrange_files()
    organizer.start_organization(categorized_file)

def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
        parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
        return parser.parse_args()

if __name__ == "__main__":
    main()