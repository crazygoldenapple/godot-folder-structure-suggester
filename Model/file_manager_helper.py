from Model.log import Logger
from pathlib import Path
import os
import json

class FileManagerHelper:
    logger = Logger(special_prefix="FileManagerHelper")
    cwd = Path.cwd()
    
    @staticmethod
    def get_file_name(file_path: str) -> str:
        FileManagerHelper.logger.info(f"Getting file name from path: {file_path}")
        file_name = os.path.basename(file_path)
        FileManagerHelper.logger.info(f"Extracted file name: {file_name}")
        return file_name
    
    @staticmethod
    def construct_path(arg1, arg2) -> str:
        path = F'{arg1}/{arg2}'
        FileManagerHelper.logger.info(f"Constructed path: {path}")
        return path
    
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
    def load_config(file_path: str = "/Configuration/default_config.json") -> dict:
        full_path = FileManagerHelper.construct_path(FileManagerHelper.cwd, file_path)
        FileManagerHelper.logger.info(f"Loading Default configuration from {full_path}.")
        try:
            config_content = FileManagerHelper.read_file(full_path)
            config = json.loads(config_content)
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
            files = FileManagerHelper.get_files(path)
            FileManagerHelper.logger.info(f"Files found in {path}: {files}")
            return files
        except FileNotFoundError:
            FileManagerHelper.logger.error(f"Directory not found: {path}")
            return []
    
    @staticmethod
    def get_files(path: str) -> list:
        FileManagerHelper.logger.info(f"Getting files recursively from: {path}")
        files = []
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                created_path = os.path.join(root, filename)
                files.append((filename, created_path))
        FileManagerHelper.logger.info(f"Files found: {files}")
        return files
