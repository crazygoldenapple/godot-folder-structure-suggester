from math import log
import re
from typing import Optional

from Model.file_manager_helper import FileManagerHelper as fm
from Model.folder_organization_helper import FolderOrganizationHelper as fo
from Model.log import Logger
from Model.tokenizer import Tokenizer
from Model.organizer_constants import OrganizerConstants
from Model.vectorizer import Vectorizer
from Model.clustering_engine import ClusteringEngine

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
        self.logger = Logger(special_prefix=OrganizerConstants.ORGANIZER.value)
        self.root_path = root_path

        self.logger.info("Initializing Organizer.")
        self.default_config = fm.load_config()

        if not self.default_config:
            self.logger.error("Default configuration could not be loaded.")

        self.custom_config = provided_config or self.default_config
        if provided_config:
            self.logger.info("Using provided configuration.")
        else:
            self.logger.info("Using default configuration.")

        self.logger.info("Organizer initialized.")

    def daily_organize_files(self) -> tuple:
        """
        Organizes files in a directory based on predefined categories and configurations.
        This function performs daily file organization by:
        - Retrieving files from the specified root directory.
        - Filtering files based on exclusion patterns defined in the configuration.
        - Classifying files into categories using custom logic.
        - Processing files based on keywords and data configurations.
        - Organizing files into a structured dictionary with subcategories.
        Returns:
            tuple: A tuple containing:
                - structure_dict (dict): A dictionary representing the organized file structure.
                - files_to_path (dict): A dictionary mapping file names to their respective paths.
        """
        self.logger.info("Starting daily file organization.")
        
        files_tuple_list = fm.get_files_from_directory(self.root_path)
        files_name_list = [name for (name, _) in files_tuple_list]
        files_to_path = {name: path for (name, path) in files_tuple_list if not any(re.search(pattern, name) for pattern in self.custom_config.get(OrganizerConstants.EXCLUDE.value, {}).get(OrganizerConstants.DEFAULT.value, []))}
        categorized_files = self._classify_files(files_name_list)
        
        structure_dict = {}
        categories = [category for category in self.custom_config if category not in [OrganizerConstants.EXCLUDE.value, OrganizerConstants.KEYWORDS.value, OrganizerConstants.DATA.value]]
    
        self._keyword_processing(categorized_files, structure_dict)
        self._data_processing(categorized_files, structure_dict)
        self._process_generic_category(categories, structure_dict, categorized_files)
        self._split_into_subcategories(structure_dict)
        
        self.logger.info(f"Daily file organization completed. {structure_dict}")
        return structure_dict, files_to_path

    def folder_struct_suggestion(self) -> dict:
        self.logger.info("Starting daily file structuring.")
        files_tuple_list = fm.read_all_directories(self.root_path)
        files_tuple_list = self._exlude_non_tokenized_files(files_tuple_list, ['exclude', 'asset'])
        
        file_to_path = {name:path for (name, path) in files_tuple_list}
        self.logger.info(f"Files to process: {len(file_to_path)}")
        
        tokenizer = Tokenizer()
        tokenized_files = tokenizer.process_files(file_to_path)
        vectorizer = Vectorizer()
        matrix = vectorizer.fit_transform(tokenized_files)
            
        self._cluster_files(matrix, vectorizer)
        
        self.logger.info("Daily file structuring completed.")
        
        return {}
    
    def _cluster_files(self, matrix, vectorizer):
        engine = ClusteringEngine(matrix, vectorizer)
        clusters = engine.cluster(k=20)

        self.logger.info("📦 File Groups:")
        for label, files in clusters.items():
            self.logger.info(f"\nCluster {label}:")
            for f in files:
                self.logger.info(f"  - {f}")

        self.logger.info("\n🏷️ Top Keywords Per Cluster:")
        top_keywords = engine.get_top_keywords_per_cluster()
        for cluster_id, words in top_keywords.items():
            self.logger.info(f"Cluster {cluster_id}: {', '.join(words)}")

    
    def _exlude_non_tokenized_files(self, files_tuple_list: list, categories: list) -> list:
        """
        Exclude files that are not tokenized based on the provided configuration.

        :param files_tuple_list: List of file tuples (name, path).
        :return: Filtered list of file tuples.
        """
        exclude_patterns = []
        for category in categories:
            exclude_patterns.extend(self.custom_config.get(category, {}).get(OrganizerConstants.DEFAULT.value, []))
            
        self.logger.debug(f"Exclusion patterns: {exclude_patterns}")
        return [
            (name, path) for name, path in files_tuple_list
            if not any(re.search(pattern, name) for pattern in exclude_patterns)
        ]
    
    def _data_processing(self, categorized_files, structure_dict):
        for tres in categorized_files.get("data", []):
            inner_text = fm.read_file(tres[1])
            match = re.search(r'script_class=".*"', inner_text)
            class_name = ''
            if match:
                class_name = match.group(0).split('"')[1]
            
            if fo.folder_exists(f"Code/Resource/{class_name}", structure_dict):
                fo.add_content(f"Code/Resource/{class_name}", structure_dict, [tres])
            else:
                fo.add_content(f"Data", structure_dict, [tres])

    def _keyword_processing(self, categorized_files, structure_dict):
        for category, files in categorized_files.items():
            self.logger.info(f"{category.capitalize()} files: {len(files)}")
            if category == "exclude":
                self.logger.info("Exclusion category found, skipping.")
                continue
            
            if category == "keywords":
                self._process_keywords_category(files, structure_dict)
            else:
                self._initialize_generic_category(category, structure_dict)


    def _process_generic_category(self, categories: list, structure_dict: dict, categorized_files: dict):
        """
        Process a generic category and organize files into the structure dictionary.

        :param category: The name of the category.
        :param structure_dict: The structure dictionary to update.
        :param files: List of files in the category.
        """
        for category in categories:
            files = categorized_files.get(category, [])
            category = category.capitalize()
            fo.add_content(category, structure_dict, files)   

    def _process_keywords_category(self, files: list, structure_dict: dict):
        """
        Process the 'keywords' category and organize files into 'Code' and 'Scene' subcategories.

        :param files: List of files in the 'keywords' category.
        :param structure_dict: The structure dictionary to update.
        """
        for folder_name in self.custom_config['keywords'][OrganizerConstants.DEFAULT.value]:
            category_files = self._filter_files_by_extension(files, [folder_name])       
            code_files = self._filter_files_by_extension(category_files, self.custom_config['code'][OrganizerConstants.DEFAULT.value])
            scene_files = self._filter_files_by_extension(category_files, self.custom_config['scene'][OrganizerConstants.DEFAULT.value])
            
            if folder_name == "Resource":
                fo.create_folder("Code/Resource", structure_dict)
                for file_name in code_files:
                    file_name_without_ext = re.sub(r'\.\w+$', '', file_name)
                    fo.add_content(f"Code/Resource/{file_name_without_ext}", structure_dict, [file_name])
            else: 
                if code_files:
                    fo.add_content(f"Code/{folder_name.capitalize()}", structure_dict, code_files)
            if scene_files:
                fo.add_content(f"Scene/{folder_name.capitalize()}", structure_dict, scene_files)

    

    def _initialize_generic_category(self, category: str, structure_dict: dict):
        """
        Process a generic category and initialize it in the structure dictionary.

        :param category: The name of the category.
        :param structure_dict: The structure dictionary to update.
        """
        category = category.capitalize()
        fo.create_folder(category, structure_dict)
        
        self.logger.info(f"Initialized category: {category}")
        
        return structure_dict
    
    def _filter_files_by_extension(self, files_name_list: list, extensions: list) -> list:        
        filtered_files = [
            name for name in files_name_list
            if any(re.search(pattern, name) for pattern in extensions)
        ]
        
        for name in filtered_files:
            self.logger.debug(f"Included file: {name} by extension filter {extensions}")

        return filtered_files
    
    def _classify_files(self, files_tuple_list) -> dict:
        self.logger.info("Starting file classification.")
        categorized_files = self._filter_and_categorize_files(files_tuple_list)
        self.logger.info("Finsished classification.")

        return categorized_files



    def _filter_and_categorize_files(self, files_name_list):
        exclude_patterns = self.custom_config.get("exclude", {})
        self.logger.debug(f"Exclusion patterns: {exclude_patterns}")

        filtered_files = self._filter_excluded_files(files_name_list, exclude_patterns.get("OrganizerConstants.DEFAULT.value", []))
        self.logger.debug(f"Files after exclusion: {filtered_files}")

        categorized_files = self._group_files_based_on_config(filtered_files)
        return categorized_files
    
    def _filter_excluded_files(self, files_name_list: list, exclude_patterns: list) -> list:
        """
        Exclude files matching any of the provided patterns.

        :param files_name_list: List of file tuples (name, path).
        :param exclude_patterns: List of regex patterns to exclude.
        :return: Filtered list of file tuples.
        """
        filtered_files = [
            name for name in files_name_list
            if not any(re.search(pattern, name) for pattern in exclude_patterns)
        ]

        excluded_files = set(files_name_list) - set(filtered_files)
        for name in excluded_files:
            self.logger.debug(f"Excluded file: {name}")

        return filtered_files

    def _group_files_based_on_config(self, files_name_list: list) -> dict:
        """
        Categorize files based on the configuration.

        :param files_name_list: List of file names
        :return: Dictionary categorizing files by type.
        """
        categorized_files = {category: [] for category in self.custom_config if category != "exclude"}

        for name in files_name_list:
            for category, patterns in self.custom_config.items():
                if category == "exclude":
                    continue

                if any(re.search(pattern, name) for pattern in patterns[OrganizerConstants.DEFAULT.value]):
                    categorized_files[category].append(name)
                    self.logger.debug(f"Categorized file: {name} as {category}")
                    break

        for category, files in categorized_files.items():
            self.logger.debug(f"{category.capitalize()} files: {len(files)}")

        return categorized_files
    
    def _split_into_subcategories(self, structure_dict: dict) -> dict:
        """
        Recursively split main categories into subcategories based on the configuration.

        :param structure_dict: The structure dictionary with main categories.
        :param config: The configuration dictionary defining subcategories and patterns.
        :return: Updated structure dictionary with subcategories.
        """
        def process_category(category_path: str, files: list, sub_config: dict):
            for sub_category, inner_data in sub_config.get('content', {}).items():
                self.logger.info(f"Processing subcategory: {sub_category} in {category_path}")
                self.logger.debug(f"Subcategory data: {inner_data}")
                sub_category_path = f"{category_path}/{sub_category.capitalize()}"
                filtered_files = self._filter_files_by_extension(files, inner_data[OrganizerConstants.DEFAULT.value])

                if filtered_files:
                    fo.add_content(sub_category_path, structure_dict, filtered_files)
                    fo.remove_content(category_path, structure_dict, filtered_files)
                    self.logger.info(f"Added {len(filtered_files)} files to subcategory '{sub_category_path}'")

                    if sub_category in config and isinstance(config[sub_category], dict):
                        process_category(sub_category_path, filtered_files, config[sub_category])

        self.logger.info("Splitting main categories into subcategories.")
        config = self.custom_config.copy()
        for main_category, files in structure_dict.items():
            if main_category.lower() in config:
                self.logger.info(f"Processing subcategories for main category: {main_category}")
                process_category(main_category, files.get('Content', []), config[main_category.lower()])
        self.logger.info("Subcategories split completed.")
        return structure_dict