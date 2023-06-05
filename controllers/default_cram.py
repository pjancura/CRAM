# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

logger = logging.getLogger("default_cram")
logger_file_name = 'default_cram.log'
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler(f"../MacOS/applications/CRAM/logs/{logger_file_name}", "a", 1000000, 5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def index(): 
    logger.info(auth.user_groups)
    return dict(message="hello from default_cram.py")

def about_us(): 
    return locals()

def team_bio():
    return locals()

