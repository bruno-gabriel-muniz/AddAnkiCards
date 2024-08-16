import logging
import os.path as path


def get_logger() -> logging.Logger:
    """
    Funcao que cria e formata os logs dos testes
    """
    logger = logging.getLogger(__name__)
    logging.FileHandler(
        path.join('.', 'LoggerMain.log'), 'w')
    hendler = logging.StreamHandler()
    hendler.setLevel(logging.WARNING)
    hendler.setFormatter(
        '%(filename)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.addHandler(hendler)
    return logger
