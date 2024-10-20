import sys

from loguru import logger


def set_logger_format():
    """
    Set the Loguru logger format to my personal preference.
    """
    FORMAT = (
        "<green>{time:MM-DD-YYYY HH:mm:ss.S}</green> | "
        "<level>{level.icon}</level> | "
        "<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    COMPILE_FORMAT = "<green>{time:MM-DD HH:mm:ss.S}</green> | <level>{message}</level>"

    logger.remove()
    logger.add(sys.stdout, format=FORMAT, level="TRACE", filter=lambda record: "compile_log" not in record["extra"])
    logger.add(sys.stdout, format=COMPILE_FORMAT, level="TRACE", filter=lambda record: "compile_log" in record["extra"])

    levels = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    for level_name in levels:
        logger.level(level_name, icon=level_name[0])

def setup_eric_env():
    """
    Set up Eric's preferred environment for any general application. Recommended to put this at the very start of any
    script.
    """
    set_logger_format()
    logger.info("Eric's work environment is all set up. Have fun coding! 🎉📣🤗")
