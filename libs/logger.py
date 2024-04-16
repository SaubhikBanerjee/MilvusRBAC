import logging
from libs.read_config import ReadConfig
from datetime import datetime


class LoggerClass:
    def __init__(self):
        config = ReadConfig("config/config.ini")
        self.file_name = (str(config.log_file_destination) +
                          str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".log")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(config.log_level)
        self.log_handler = logging.FileHandler(self.file_name)
        self.log_handler.setLevel(config.log_level)
        self.log_formatter = logging.Formatter(config.log_format, "%Y-%m-%d %H:%M:%S")
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.consoleHandler)

    def set_logger(self):
        return self.logger
