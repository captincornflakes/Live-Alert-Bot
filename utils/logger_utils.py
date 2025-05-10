import logging
from datetime import datetime

# Configure the logger
logging.basicConfig(
    filename="events.log",  # Log file name
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

def log_event(message, level="info"):
    """
    Log an event message with the specified log level.

    Args:
        message (str): The message to log.
        level (str): The log level ('info', 'warning', 'error', 'debug').
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"

    if level.lower() == "info":
        logging.info(log_message)
    elif level.lower() == "warning":
        logging.warning(log_message)
    elif level.lower() == "error":
        logging.error(log_message)
    elif level.lower() == "debug":
        logging.debug(log_message)
    else:
        logging.info(log_message)  # Default to info level