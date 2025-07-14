import json
import re
import json
from typing import Optional
from Model.file_manager_helper import FileManagerHelper
from Model.log import Logger

class Organizer:
    """
    Organizes files in a directory based on a provided or default configuration.
    """

    def __init__(self, root_path: str, provided_config: Optional[dict] = None):
        """
        Initialize the Organizer with a root path and configuration.

        :param root_path: The root directory to organize.
        :param provided_config: Optional custom configuration for organizing files.
        """
        self.logger = Logger(special_prefix="Organizer")
        self.root_path = root_path

        self.logger.info("Initializing Organizer.")
        self.default_config = FileManagerHelper.load_config()

        if not self.default_config:
            self.logger.error("Default configuration could not be loaded.")

        self.custom_config = provided_config or self.default_config
        if provided_config:
            self.logger.info("Using provided configuration.")
        else:
            self.logger.info("Using default configuration.")

        self.logger.info("Organizer initialized.")

    def classify_files(self) -> dict:
        """
        Organize files in the root directory based on the configuration.

        :return: A dictionary categorizing files by type.
        """
        self.logger.info("Starting file organization.")

        files_tuple_list = FileManagerHelper.read_all_directories(self.root_path)
        exclude_patterns = self.custom_config.get("exclude", [])
        self.logger.debug(f"Exclusion patterns: {exclude_patterns}")

        filtered_files = self._filter_excluded_files(files_tuple_list, exclude_patterns)
        self.logger.debug(f"Files after exclusion: {filtered_files}")

        categorized_files = self._group_files_based_on_config(filtered_files)
        self.logger.info("File organization completed.")

        return categorized_files

    def get_new_project_structure(self) -> dict:
        return {}

    def _filter_excluded_files(self, files_tuple_list: list, exclude_patterns: list) -> list:
        """
        Exclude files matching any of the provided patterns.

        :param files_tuple_list: List of file tuples (name, path).
        :param exclude_patterns: List of regex patterns to exclude.
        :return: Filtered list of file tuples.
        """
        filtered_files = [
            (name, path) for name, path in files_tuple_list
            if not any(re.search(pattern, name) for pattern in exclude_patterns)
        ]

        excluded_files = set(files_tuple_list) - set(filtered_files)
        for name, _ in excluded_files:
            self.logger.debug(f"Excluded file: {name}")

        return filtered_files

    def _group_files_based_on_config(self, files_tuple_list: list) -> dict:
        """
        Categorize files based on the configuration.

        :param files_tuple_list: List of file tuples (name, path).
        :return: Dictionary categorizing files by type.
        """
        categorized_files = {category: [] for category in self.custom_config if category != "exclude"}

        for name, path in files_tuple_list:
            for category, patterns in self.custom_config.items():
                if category == "exclude":
                    continue

                if any(re.search(pattern, name) for pattern in patterns):
                    categorized_files[category].append((name, path))
                    self.logger.debug(f"Categorized file: {name} as {category}")
                    break

        for category, files in categorized_files.items():
            self.logger.debug(f"{category.capitalize()} files: {len(files)}")

        return categorized_files