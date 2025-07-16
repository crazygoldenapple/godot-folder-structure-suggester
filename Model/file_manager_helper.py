from Model.log import Logger
from pathlib import Path
import os
import json

class FileManagerHelper:
    logger = Logger(special_prefix="FileManagerHelper")
    cwd = Path.cwd()
    
    @staticmethod
    def save_file(data, file_path: str, file_name: str) -> None:
        FileManagerHelper.logger.info(f"Saving data to file: {file_path}")
        FileManagerHelper.create_path(file_path)
        file_path = FileManagerHelper.construct_path(FileManagerHelper.cwd,file_path, file_name)
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            FileManagerHelper.logger.info(f"Data saved successfully to {file_path}")
        except IOError as e:
            FileManagerHelper.logger.error(f"Error saving file {file_path}: {e}")
    
    @staticmethod
    def load_json_file(file_path: str) -> dict:
        FileManagerHelper.logger.info(f"Loading file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            FileManagerHelper.logger.info(f"File loaded successfully from {file_path}")
            return data
        except FileNotFoundError:
            FileManagerHelper.logger.error(f"File {file_path} not found.")
            return {}
        except json.JSONDecodeError as e:
            FileManagerHelper.logger.error(f"Error decoding JSON from file {file_path}: {e}")
            return {}
    
    @staticmethod
    def get_file_name(file_path: str) -> str:
        FileManagerHelper.logger.info(f"Getting file name from path: {file_path}")
        file_name = os.path.basename(file_path)
        FileManagerHelper.logger.info(f"Extracted file name: {file_name}")
        return file_name
    
    @staticmethod
    def construct_path(*args) -> str:
        path_parts = []
        for arg in args:
            path_parts.extend(str(arg).split('/'))
        FileManagerHelper.logger.debug(f"Path Parts: {path_parts}")
        path = "/".join([part for part in path_parts if len(part) > 0])
        FileManagerHelper.logger.info(f"Constructed path: {path}")
        return "/" + path
    
    @staticmethod
    def directory_exists(dir_path) -> bool:
        FileManagerHelper.logger.info(f"Checking if directory exists: {dir_path}")
        exists = os.path.isdir(dir_path)
        FileManagerHelper.logger.info(f"Directory exists: {exists}")
        return exists
    
    @staticmethod
    def file_exists(file_path) -> bool:
        FileManagerHelper.logger.info(f"Checking if file path exists: {file_path}")
        exists = os.path.exists(file_path)
        FileManagerHelper.logger.info(f"File exists: {exists}")
        return exists

    @staticmethod
    def read_file(file_path: str) -> str:
        FileManagerHelper.logger.info(f"Reading file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            FileManagerHelper.logger.info(f"Read content from {file_path}: {content[:50]}...")
            return content
        except FileNotFoundError:
            FileManagerHelper.logger.error(f"File {file_path} not found.")
            return ""
        except IOError as e:
            FileManagerHelper.logger.error(f"Error reading file {file_path}: {e}")
            return ""
    
    @staticmethod
    def load_config(file_path: str = "Configuration/default_config.json") -> dict:
        full_path = FileManagerHelper.construct_path(FileManagerHelper.cwd, file_path)
        FileManagerHelper.logger.info(f"Loading Default configuration from {full_path}.")
        try:
            config = FileManagerHelper.load_json_file(full_path)
            FileManagerHelper.logger.info("Configuration loaded successfully.")
            return config
        except FileNotFoundError:
            FileManagerHelper.logger.error(f"Configuration file {full_path} not found.")
            return {}
        except json.JSONDecodeError:
            FileManagerHelper.logger.error(f"Error decoding JSON from the file {full_path}.")
            return {}
    
    @staticmethod
    def create_path(path: str) -> None:
        FileManagerHelper.logger.info(f"Creating path: {path}")
        os.makedirs(path, exist_ok=True)
        FileManagerHelper.logger.info(f"Path created: {path}")
    
    @staticmethod
    def read_all_directories(path: str = '') -> list:
        FileManagerHelper.logger.info(f"Reading directory: {path}")
        try:
            files = FileManagerHelper.collect_files_recursively(path)
            FileManagerHelper.logger.info(f"Files found in {path}: {files}")
            return files
        except FileNotFoundError:
            FileManagerHelper.logger.error(f"Directory not found: {path}")
            return []
    
    @staticmethod
    def collect_files_recursively(path: str) -> list:
        FileManagerHelper.logger.info(f"Getting files recursively from: {path}")
        files = []
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                created_path = os.path.join(root, filename)
                files.append((filename, created_path))
        FileManagerHelper.logger.info(f"Files found: {files}")
        return files

    @staticmethod
    def get_files_from_directory(directory: str) -> list:
        FileManagerHelper.logger.info(f"Getting files from directory: {directory}")
        if not os.path.isdir(directory):
            FileManagerHelper.logger.error(f"Directory does not exist: {directory}")
            return []
        
        files = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append((entry, full_path))
        
        FileManagerHelper.logger.info(f"Files found in directory {directory}: {files}")
        return files