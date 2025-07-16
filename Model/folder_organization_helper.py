from Model.log import Logger


class FolderOrganizationHelper:
    logger = Logger(special_prefix="FolderOrganizationHelper")
    
    
    @staticmethod
    def create_folder(path: str, folder_tree: dict) -> None:
        path_parts = path.split('/')
        last_path = ""
        for part in path_parts:
            part = part.capitalize()
            if part not in folder_tree:
                folder_tree[part] = {"Content": []}
                last_path += "/" + part
                FolderOrganizationHelper.logger.info(f"Created folder: {last_path}")
            folder_tree = folder_tree[part]
    
    @staticmethod
    def add_content(path: str, folder_tree: dict, content: list) -> None:
        FolderOrganizationHelper.create_folder(path, folder_tree)
        path_parts = path.split('/')
        for part in path_parts:
            part = part.capitalize()
            if part not in folder_tree:
                FolderOrganizationHelper.logger.error(f"Folder '{part}' does not exist in the tree.")
                return
            folder_tree = folder_tree[part]
        folder_tree["Content"].extend(content)
        FolderOrganizationHelper.logger.info(f"Added content to folder: {path}")
        
    @staticmethod
    def remove_content(path: str, folder_tree: dict, content_to_remove: list) -> None:
        path_parts = path.split('/')
        for part in path_parts:
            part = part.capitalize()
            if part not in folder_tree:
                FolderOrganizationHelper.logger.error(f"Folder '{part}' does not exist in the tree.")
                return
            folder_tree = folder_tree[part]
        content = folder_tree.get("Content", [])
        for item in content_to_remove:
            if item in content:
                content.remove(item)
                FolderOrganizationHelper.logger.info(f"Removed '{item}' from folder: {path}")
            else:
                FolderOrganizationHelper.logger.warning(f"Item '{item}' not found in folder: {path}")


    @staticmethod
    def folder_exists(path: str, folder_tree: dict) -> bool:
        path_parts = path.split('/')
        for part in path_parts:
            part = part.capitalize()
            if part not in folder_tree:
                return False
            folder_tree = folder_tree[part]
        return True