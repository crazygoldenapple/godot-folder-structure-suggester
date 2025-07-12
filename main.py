import json
import argparse
import os
from Model.log import log
from pathlib import Path
import re

logger = log()

def load_config(file_path = "Congfiguration/default_config.json"):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the file {file_path}.")
        return {}


def main():
    config = load_config()
    result = validate_configuration(config)
    
    if not result:
        return
    
    root_path = parse_args().path
    logger.info(f"Root path for organization: {root_path}")
    
    tscn_files, code_files, assets_files = arrange_files(config, root_path)
    organize_files(root_path, tscn_files, code_files, assets_files)

def organize_files(root_path, tscn_files, code_files, assets_files):
    return

def arrange_files(config, root_path) -> tuple:
    logger.info("Organizing files based on configuration.")
    
    files_list = os.listdir(root_path)
    logger.debug(f"Files found in {root_path}: {files_list}")
    
    exlude_files = config.get("exclude", [])
    logger.debug(f"Files to exclude: {exlude_files}")
    
    files_list = exclude_files(files_list, exlude_files)
    files_list = [file for file in files_list if not os.path.isdir(os.path.join(root_path, file))]
    logger.debug(f"Files after exclusion: {files_list}")
    
    return separate_files(files_list, config)
    
    
    
    
    logger.info("File organization completed successfully.")

def separate_files(files_list, config):
    tres_files = [file for file in files_list if re.fullmatch(r".*\.tscn$", file)]
    code_files = [file for file in files_list if re.fullmatch(r".*\.cs$", file)]
    assets_files = set(files_list) - set(tres_files) - set(code_files)
    
    logger.debug(f"Tres files: {tres_files}")
    logger.debug(f"Code files: {code_files}")
    logger.debug(f"Assets files: {assets_files}")
    
    return tres_files, code_files, assets_files

def exclude_files(files_list, exclude):
    filtered_files = [file for file in files_list if not any(re.fullmatch(pattern, file) for pattern in exclude)]
    return filtered_files

def validate_configuration(config) -> bool:
    logger.info("Configuration loaded from default path.")
    if not config:
        logger.warning("No configuration loaded")
        return False
    
    logger.info("Configuration loaded successfully.")
    logger.debug(f"Configuration: {config}")
    return True
    
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sort project files into basic folders.")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Root path of the project (default is current directory).")
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("Starting the application ")
    main()
    logger.info("Application finished ")