from pathlib import Path
from Model.organizer import Organizer
from Model.file_manager import FileManager
from Model.file_manager_helper import FileManagerHelper
from Model.string_extention import StringExtention
import argparse

def main():
    root_path = parse_args().path
    file_manager = FileManager(root_path)
    organizer = Organizer(file_manager)
    categorized_file = organizer.arrange_files()
    scene_to_resource, special_scene, scene_dependencies = organizer.map_scenes_to_resources(categorized_file)
    organizer.organize_project(scene_to_resource, special_scene, scene_dependencies)

def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
        parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
        return parser.parse_args()

if __name__ == "__main__":
    main()