from __future__ import annotations
from .config.config import Config
from .library import set_config
from .__header__ import __header__
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

# Load User Defined Config
DEFAULT_CONFIG_PATH = f'~/.config/{__header__.lower()}'
CONFIG_PATH = os.environ.get(f'{__header__}_CONFIG_PATH', DEFAULT_CONFIG_PATH)
CONFIG = Config(CONFIG_PATH)

# Logging Configuration
logger = logging.getLogger(__header__)
set_config(CONFIG, 'logging.path')
set_config(
    CONFIG,
    'logging.format',
    '%(asctime)s - %(module)s:%(lineno)s - %(levelname)s - %(message)s',
)
set_config(CONFIG, 'logging.level', 'INFO')
loghandler_sys = logging.StreamHandler(sys.stdout)

if CONFIG.logging_path:
    set_config(CONFIG, 'logging.backup_count', 3, int)
    set_config(CONFIG, 'logging.rotate_bytes', 512000, int)
    loghandler_file = RotatingFileHandler(
        os.path.expanduser(CONFIG.logging_path),
        'a',
        CONFIG.logging_rotate_bytes,
        CONFIG.logging_backup_count
    )
    loghandler_file.setFormatter(logging.Formatter(CONFIG.logging_format))
    logger.addHandler(loghandler_file)

loghandler_sys.setFormatter(logging.Formatter(CONFIG.logging_format))
logger.addHandler(loghandler_sys)
logger.setLevel(CONFIG.logging_level)

for msg in CONFIG.deferred_messages:
    logger.info(msg)
CONFIG.reset_log()
