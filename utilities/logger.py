import logging
import os

class SetupLogger:
    def __init__(self, logger_name, log_file):
        self.logger_name = logger_name
        self.log_file = log_file
    
    def create_logger(self):
        log_directory = os.path.dirname(self.log_file)
        os.makedirs(log_directory, exist_ok=True)
        
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(self.log_file)
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
        return logger
