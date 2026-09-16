import logging
import configparser
import os

#### Base setup of functions
def loadset(path="settings.ini"):
    ########### Load settngs from path ###########
    kitConfig = configparser.ConfigParser()
    # If the file doesn't exist, we can provide defaults here
    if os.path.exists(path):
        kitConfig.read(path)
    else:
        print(f"Warning: {path} not found. Using defaults.")
    return kitConfig


def setlogger(kitSettings):

    logpath = kitSettings["kitpaths"]["logpath"]

    level = logging.getLevelNamesMapping()[
        kitSettings["kitsettings"]["loglevel"]
    ]

    logger = logging.getLogger()
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "{asctime} - {name} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler(logpath)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

