import logging.handlers
import os

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'parser.log')

STEAM_HANDLER = logging.StreamHandler()
STEAM_HANDLER.setFormatter(LOGGING_FORMATTER)
STEAM_HANDLER.setLevel(LOGGING_LEVEL)

FILE_HANDLER = logging.handlers.RotatingFileHandler(PATH, maxBytes=1000000, backupCount=10)
FILE_HANDLER.suffix = '%d-%m-%Y'
FILE_HANDLER.setFormatter(LOGGING_FORMATTER)

LOGGER = logging.getLogger('parser')
LOGGER.addHandler(STEAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
