import logging
import os

class log:
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    
    def __init__(self, folder_path='Logs', file_name='project_log.log'):
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        for level in self.levels:
            logging.basicConfig(filename= folder_path + '/' + file_name, level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
        self.logger = logging.getLogger(__name__)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)