from logging import Logger, Formatter
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    log_file_folder = os.getcwd() + "//logs"
    os.makedirs(log_file_folder, exist_ok=True)
    
    log_file_path = log_file_folder + "//app.log"

    handler = TimedRotatingFileHandler(
        filename=log_file_path, when="d", interval=1)
    
    formatter = Formatter(
        fmt="%(levelname)s %(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s"
    )
    handler.setFormatter(formatter)

    logger = Logger('app')
    logger.setLevel(10)
    logger.handlers = []
    logger.addHandler(handler)

    return logger

log = setup_logger()