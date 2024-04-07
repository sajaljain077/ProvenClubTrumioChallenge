import logging

logger = logging.getLogger()
logger.setLevel("DEBUG")
formatter = '%(levelname)s - %(message)s'
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(formatter))
logger.addHandler(consoleHandler)


