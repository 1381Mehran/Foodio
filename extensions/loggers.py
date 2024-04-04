import os
import logging

from django.conf import settings


# Defining Logger formatter

formatter = logging.Formatter('* %(levelname)s - %(asctime)s * %(filename)s -> %(lineno)d , %(message)s')

# loggers
logger_info = logging.getLogger('info_logger')
logger_info.setLevel(logging.INFO)

logger_error = logging.getLogger('error_logger')
logger_error.setLevel(logging.ERROR)


# handlers

if not os.path.isdir(f'{settings.BASE_DIR}/logs'):
    os.mkdir(f'{settings.BASE_DIR}/logs')

file_handler_info = logging.FileHandler(f'{settings.BASE_DIR}/logs/INFO.log')
file_handler_info.setFormatter(formatter)
logger_info.addHandler(file_handler_info)

file_handler_error = logging.FileHandler(f'{settings.BASE_DIR}/logs/ERROR.log')
file_handler_error.setFormatter(formatter)
logger_error.addHandler(file_handler_error)





