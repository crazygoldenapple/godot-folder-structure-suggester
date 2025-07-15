from Model.log import Logger
from Model.file_manager_helper import FileManagerHelper

class MLRefactorSuggestor:
    logger = Logger(special_prefix="MLRefactorSuggestion")
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.custom_config = FileManagerHelper.load_config()