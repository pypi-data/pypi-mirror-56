import logging
from typing import Callable


class KilobaikLogger:
    def __init__(self, logger_name: str, level: str,
                 formatter: str = '%(levelname)s | %(name)s - %(asctime)s: '
                                  '[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'):
        self.logger_name = logger_name
        self.formatter = logging.Formatter(formatter)
        self.logging_level = KilobaikLogger.get_logging_level(level)

        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.logging_level)
        self.attach_console_logging_handler()

    def __repr__(self):
        return '{name}(level={level})'.format(name=KilobaikLogger.__name__, level=self.logging_level)

    def attach_console_logging_handler(self):
        console = logging.StreamHandler()
        self.attach_handler(console)

    def attach_handler(self, handler: logging.Handler):
        handler.setLevel(self.logging_level)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)

    def fatal(self, message, *args, **kwargs):
        self.logger.fatal(message, *args, **kwargs)

    def warn(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    @staticmethod
    def get_logging_level(level: str):
        if level is not None:
            if level.upper() in ['CRITICAL', 'FATAL']:
                return logging.CRITICAL
            elif level.upper() in ['WARNING', 'WARN']:
                return logging.WARNING
            elif level.upper() == 'ERROR':
                return logging.ERROR
            elif level.upper() == 'INFO':
                return logging.INFO
            elif level.upper() == 'DEBUG':
                return logging.DEBUG

        return logging.NOTSET

    @staticmethod
    def attach(label: str, level: str):
        def _attach(function: Callable):
            if 'logger' not in function.__globals__:
                logger = KilobaikLogger(label, level)
                function.__globals__['logger'] = logger
            return function
        return _attach
