import array
from pathlib import Path
from venv import logger

from numpy import full
from Model.log import Logger
import json
import re
import os

class Organizer:
    special_keywords = ["Manager", "Component", "Global", "UI"]
    
    def __init__(self, root_path: Path, cwd: Path,config: dict= None):
        self.logger = Logger()
        self.root_path = root_path
        self.cwd = cwd

        if config is None:
            self.logger.info("No configuration provided.")
            default_config = self.load_config()
            if default_config is None:
                logger.error("Default configuration could not be loaded.")
            self.config = default_config
        else:
            self.config = config
        
        self.logger.info("Organizer initialized.")
    
    def arrange_files(self) -> dict:
        logger.info("Organizing files based on configuration.")
        
        files_list = os.listdir(self.root_path)
        logger.debug(f"Files found in {self.root_path}: {files_list}")
        
        exlude_files = self.config.get("exclude", [])
        logger.debug(f"Files to exclude: {exlude_files}")
        
        files_list = self._exclude_files(files_list, exlude_files)
        files_list = [file for file in files_list if not os.path.isdir(os.path.join(self.root_path, file))]
        logger.debug(f"Files after exclusion: {files_list}")
    
        return self._separate_files(files_list)
    
    def load_config(self, file_path: str = "/Configuration/default_config.json") -> dict:
        full_path = f"{self.cwd}{file_path}"
        self.logger.info(f"Loading Default configuration from {full_path}.")
        try:
            with open(full_path, 'r') as file:
                config = json.load(file)
            self.logger.info("Configuration loaded successfully.")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file {full_path} not found.")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from the file {full_path}.")
            return None

    def start_organization(self, categorized_files: dict):
        scene_category = "scene"
        scene_to_resources: dict = {}
        
        for c_file in categorized_files[scene_category]:
            file_path = os.path.join(self.root_path, c_file)
            with open(file_path, 'r') as file:
                content = file.read()
                matches = re.findall(r'"res://.*?"', content)
                self.logger.info(f"Found matches in {c_file}: {matches}")
                scene_to_resources[c_file] = matches
        self.logger.info(f"Scene to resources mapping: {scene_to_resources}")
        
        special_nodes = {}
        for special_keyword in self.special_keywords:
            for scene_file in categorized_files[scene_category]:
                if special_keyword in scene_file:
                    self.logger.info(f"Special keyword '{special_keyword}' found in scene '{scene_file}''.")
                    if (special_keyword not in special_nodes):
                        special_nodes[special_keyword] = []
                    special_nodes[special_keyword].append(scene_file)
        self.logger.info(f"Special nodes found: {special_nodes}")

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
                logger.debug(f"{category.capitalize()} files: {files}")
            
            return categorized_files
    
    def _validate_configuration(self, config) -> bool:
        self.logger.info("Configuration loaded from default path.")
        if not config:
            self.logger.warning("No configuration loaded")
            return False
        
        self.logger.info("Configuration loaded successfully.")
        self.logger.debug(f"Configuration: {config}")
        return True