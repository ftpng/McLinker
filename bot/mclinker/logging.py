import logging
from enum import Enum


class LogLevel(Enum):
    """
    Enum representing logging levels for clarity and maintainability.
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


RESET = "\033[0m"
DARK_GRAY = "\033[90m"       
WHITE = "\033[37m"           
LEVEL_COLORS = {
    LogLevel.DEBUG: "\033[35m",    
    LogLevel.INFO: "\033[34m",       
    LogLevel.WARNING: "\033[33m",    
    LogLevel.ERROR: "\033[31m",      
    LogLevel.CRITICAL: "\033[41m",   
}


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds colors to log messages based on level.
    """
    format_str: str = "%(asctime)s %(levelname)s     %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with timestamp, level, message, and color.

        :param record: The log record to format.
        :return: The formatted and colored log message.
        """
        base_formatter = logging.Formatter(self.format_str, "%Y-%m-%d %H:%M:%S")

        level = LogLevel(record.levelno)
        level_color = LEVEL_COLORS.get(level, RESET)
        record.levelname = f"{level_color}{record.levelname}{RESET}"
        record.msg = f"{WHITE}{record.getMessage()}{RESET}"

        formatted = base_formatter.format(record)

        if hasattr(record, 'asctime'):
            formatted = formatted.replace(record.asctime, f"{DARK_GRAY}{record.asctime}{RESET}", 1)

        return formatted


def get_logger(name: str = "MatchMaker", level: int = logging.DEBUG) -> logging.Logger:
    """
    Create or retrieve a logger with colored console output.

    :param name: Name of the logger.
    :param level: Logging level (e.g., logging.DEBUG, logging.INFO).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(ColoredFormatter())
        logger.addHandler(ch)
    return logger

logger: logging.Logger = get_logger()