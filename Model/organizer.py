from pathlib import Path
from venv import logger
from Model.file_manager import FileManager
from Model.file_manager_helper import FileManagerHelper
from Model.log import Logger
from Model.string_extention import StringExtention as se
import re

class Organizer:
    special_keywords = ["Manager", "Component", "Global", "UI"]
    
    def __init__(self, file_manager: FileManager ,config: dict= None):
        self.logger = Logger(special_prefix="Organizer")
        self.file_manager = file_manager

        if config is None:
            self.logger.info("No configuration provided.")
            default_config = FileManagerHelper.load_config()
            if default_config is None:
                logger.error("Default configuration could not be loaded.")
            self.config = default_config
        else:
            self.config = config
        
        self.logger.info("Organizer initialized.")
    
    def arrange_files(self) -> dict:
        self.logger.info("Organizing files based on configuration.")
        
        files_list = self.file_manager.read_directory()
        
        exclude_files = self.config.get("exclude", [])
        self.logger.debug(f"Files to exclude: {exclude_files}")
        
        files_list = self._exclude_files(files_list, exclude_files)
        files_list = [file for file in files_list if not self.file_manager.directory_exists(file)]
        self.logger.debug(f"Files after exclusion: {files_list}")
    
        return self._separate_files(files_list)

    def map_scenes_to_resources(self, categorized_files: dict) -> tuple:
        scene_category = "scene"
        scene_resource_mapping: dict = {}
        
        for c_file in categorized_files[scene_category]:
            content = self.file_manager.read_file(c_file)
            matches = re.findall(r'"res://.*?"', content)
            self.logger.info(f"Found matches in {c_file}: {matches}")
            scene_resource_mapping[c_file] = matches
        
        special_nodes = {}
        for special_keyword in self.special_keywords:
            for scene_file in categorized_files[scene_category]:
                if special_keyword in scene_file:
                    self.logger.info(f"Special keyword '{special_keyword}' found in scene '{scene_file}''.")
                    if special_keyword not in special_nodes:
                        special_nodes[special_keyword] = []
                    special_nodes[special_keyword].append(scene_file)
        
        scene_dependencies = {}
        for scene, resources in scene_resource_mapping.items():
            for resource in resources:
                if resource not in scene_dependencies:
                    scene_dependencies[resource] = []
                scene_dependencies[resource].append(scene)
        
        scene_to_resoure: dict = {}
        for scene, _ in scene_resource_mapping.items():
            scene_to_resoure[scene] = self.file_manager.reconstruct_local_path_to_godot(scene)
        
        self.logger.info(f"Scene to resources mapping: {scene_to_resoure}")
        self.logger.info(f"Special nodes found: {special_nodes}")
        self.logger.info(f"Scene dependencies: {scene_dependencies}")

        return scene_to_resoure, special_nodes, scene_dependencies
    
    def organize_project(self, scene_to_resources: dict, special_nodes: dict, scene_dependencies: dict) -> None:
        self._organize_special_nodes(scene_to_resources, special_nodes, scene_dependencies)
        self._organize_remain_scenes(scene_to_resources, scene_dependencies)
    
    def _organize_special_nodes(self, scene_to_resources: dict, special_nodes: dict, scene_dependencies: dict) -> None:
        for special_keyword, scenes in special_nodes.items():
            self.logger.info(f"Organizing special nodes for keyword '{special_keyword}': {scenes}")
            for scene in scenes:
                if scene in scene_dependencies:
                    dependencies = scene_dependencies[scene]
                    self.logger.info(f"Scene '{scene}' has dependencies: {dependencies}")
                    new_path = self.file_manager.create_path(self.file_manager.create_path(se.to_pascal_case(special_keyword), se.to_pascal_case(scene)))
                    self.logger.info(f"Creating new path for special node '{special_keyword}': {new_path}")
        return
    
    def _organize_remain_scenes(self, scene_to_resources: dict, scene_dependencies: dict) -> None:
        return

    def _exclude_files(self, files_list, exclude):
        filtered_files = [file for file in files_list if not any(re.fullmatch(pattern, file) for pattern in exclude)]
        return filtered_files

    def _separate_files(self, files_list):
        categorized_files = {category: [] for category in self.config if category != "exclude"}
        
        for file in files_list:
            for category, extensions in self.config.items():
                if category == "exclude":
                    continue
                if any(file.endswith(ext) for ext in extensions):
                    categorized_files[category].append(file)
                    break
        
        for category, files in categorized_files.items():
            self.logger.debug(f"{category.capitalize()} files: {files}")
        
        return categorized_files