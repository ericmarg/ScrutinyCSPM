import logging
from omegaconf import DictConfig, OmegaConf


def add_logging(cls):
    cls.logger = logging.getLogger(cls.__name__)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    cls.log_debug = log_debug
    cls.log_info = log_info
    cls.log_warning = log_warning
    cls.log_error = log_error

    return cls