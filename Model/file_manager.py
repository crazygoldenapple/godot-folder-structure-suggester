from Model.file_manager_helper import FileManagerHelper
from Model.log import Logger
import os

class FileManager:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.logger = Logger(special_prefix="FileManager")
    
    def create_path(self, path: str) -> None:
        path = self._construct_path(path)
        self.logger.info(f"Creating path: {path}")
        os.makedirs(path, exist_ok=True)
        self.logger.info(f"Path created: {path}")
    
    def directory_exists(self, dir_name: str = '') -> bool:
        dir_path = self._construct_path(dir_name)
        self.logger.info(f"Checking if directory exists: {dir_path}")
        exists = os.path.isdir(dir_path)
        self.logger.info(f"Directory exists: {exists}")
        return exists
    
    def get_file_name(self, file_path: str) -> str:
        self.logger.info(f"Getting file name from path: {file_path}")
        file_name = os.path.basename(file_path)
        self.logger.info(f"Extracted file name: {file_name}")
        return file_name
    
    def read_directory(self, dir_name: str = '') -> list:
        dir_path = self._construct_path(dir_name)
        self.logger.info(f"Reading directory: {dir_path}")
        try:
            files = os.listdir(dir_path)
            self.logger.info(f"Files found in {dir_path}: {files}")
            return files
        except FileNotFoundError:
            self.logger.error(f"Directory not found: {dir_path}")
            return None
    
    def reconstruct_godot_path_to_local(self, path: str) -> str:
        self.logger.info(f"Reconstructing Godot path to local: {path}")
        if path.startswith("res://"):
            path = path.replace("res://", "")
        local_path = self._construct_path(path)
        self.logger.info(f"Reconstructed local path: {local_path}")
        return local_path

    def reconstruct_local_path_to_godot(self, path: str) -> str:
        self.logger.info(f"Reconstructing local path to Godot: {path}")
        path = FileManagerHelper.construct_path('res:/', path)
        self.logger.info(f"Reconstructed Godot path: {path}")
        return path
    
    
    def read_file(self, file_name) -> str:
        self.logger.info(f"Reading file: {file_name}")
        file_path = self._construct_path(file_name)
        with open(file_path, 'r') as file:
            content = file.read()
        self.logger.info(f"Read content from {file_name}: {content[:50]}...")
        return content

    def write_file(self, file_name, content: str) -> None:
        self.logger.info(f"Writing to file: {file_name}")
        file_path = self._construct_path(file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        self.logger.info(f"Written content to {file_name}: {content[:50]}...")

    def replace_in_file(self, file_name, old_content: str, new_content: str) -> None:
        self.logger.info(f"Replacing content in file: {file_name}")
        file_path = self._construct_path(file_name)
        with open(file_path, 'r') as file:
            content = file.read()
        self.logger.info(f"Original content: {content[:50]}...")
        content = content.replace(old_content, new_content)
        with open(file_path, 'w') as file:
            file.write(content)
        self.logger.info(f"Replaced '{old_content}' with '{new_content}' in {file_name}")

    def append_to_file(self, file_name, content: str) -> None:
        self.logger.info(f"Appending to file: {file_name}")
        file_path = self._construct_path(file_name)
        with open(file_path, 'a') as file:
            file.write(content)
        self.logger.info(f"Appended content to {file_name}: {content[:50]}...")
    
    def _construct_path(self, *args) -> str:
        path = os.path.join(self.project_root, *args)
        self.logger.info(f"Constructed path: {path}")
        return path
