import functools
import logging
import os


# Configure logging to save logs in the "logs" folder
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join('log', 'app.log'), mode='w')
    ]
)
def logger_decorator(func):
    """
    Creates a logger decorator which logs information about function calls within the codebase
    Input: A function
    Output: A wrapper function
    Postconditions: None
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log function call details
        logging.info(f"Called {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            # Log the result
            logging.info(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            # Log any exception that occurs
            logging.error(f"{func.__name__} raised an exception: {e}")
            raise
    return wrapper
