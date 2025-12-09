import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with a specified name and log file."""
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Example usage
# logger = setup_logger('my_logger', 'my_log_file.log')
# logger.info('This is an info message')