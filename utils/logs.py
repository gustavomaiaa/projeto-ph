import logging
from logging.handlers import RotatingFileHandler
import os

# Garante que a pasta de logs exista
os.makedirs('logs', exist_ok=True)

# Configura o logger
logger = logging.getLogger('ph_logger')
logger.setLevel(logging.INFO)

# Handler para arquivo com rotação (5 arquivos de até 1MB)
file_handler = RotatingFileHandler('logs/ph_app.log', maxBytes=1_000_000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Formato dos logs
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

# Evita múltiplos handlers duplicados
if not logger.hasHandlers():
    logger.addHandler(file_handler)
