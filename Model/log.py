import logging
import os
import time

class Logger:
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    
    def __init__(self, folder_path='Logs', file_name='project_log.log', special_prefix=''):
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        
        full_path = f'{folder_path}/{time.strftime("%Y-%m-%d_%H-%M-%S")}_{file_name}'
        for level in self.levels:
            logging.basicConfig(filename=full_path, level=level, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
        self.logger = logging.getLogger(special_prefix)

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