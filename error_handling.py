"""
Error Handling Helper Class for the Mogavity Programming Language
Created by Clarissa V, and Hisao Y
April 2022
Usage for the Compiler´s Design Course
"""
import logging
import sys


def error(message: str) -> None:
    """
    Input message to output as an error in the logs.
    :param message: Message to display.
    :return: None
    """
    logging.error(message)  # use raise?
    sys.exit()


def warning(message: str):
    """
    Input message to output as a warning in the logs.
    :param message: Message to display.
    :return: None
    """
    logging.warning(message)


def info(message: str):
    """
    Input message to output as an information message in the logs.
    :param message: Message to display.
    :return: None
    """
    logging.info(message)
