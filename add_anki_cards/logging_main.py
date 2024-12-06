"""Modulo que gerencia os logs do programa."""
from logging import Logger
from os import path

from loguru import logger


def get_logger(user: str = 'User_Default') -> Logger:
    """Func. q cria e formata os logs."""
    logger.add(
        path.join(
            path.expanduser('~'), '.AddAnkiCardsData', user, 'aac_logger.txt'
        ),
        level='INFO',
        format='{time} -> {name} -> {file} -> {line} : '
        + '{level} | {message}',
    )
    return logger
