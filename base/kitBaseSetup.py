import logging
import configparser
import os
import sys

#### Base setup of functions
def loadset(path="settings.ini"):
    """ Function to create a configParser setting object for settings."""
    kitConfig = configparser.ConfigParser()
    # If the file doesn't exist just exit with the warning.
    if os.path.exists(path):
        try:
            kitConfig.read(path)
        except Exception as e:
            print(f"Warning: Failed to read settings, is {path} a readable .ini?")
            print(f"{type(e).__name__}: {e}")
    else:
        print(f"Warning: does {path} exist?")
        sys.exit()
    return kitConfig

def writeset(path: str, kitsettings: configparser):
    """ Writes the settings provided via a configparser object """
    if os.path.exists(path):
        try:
            with open(path, 'w') as configfile:
                kitsettings.write(configfile)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
    else:
        print(f"Warning: Failed to read settings, does {path} exist?")


def setlogger(kitSettings):
    """ Logger object for the whole KIT app."""

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

