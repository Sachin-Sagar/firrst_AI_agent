# logger_config.py

# This new module provides a centralized function to configure
# a shared logger for the entire agent application.

import os
import logging
import datetime

def setup_logger(verbose=False):
    """
    Sets up a global logger for the agent.

    This function configures a logger named 'agent_logger'. It creates a 
    timestamped log file in the 'logs/' directory for every run and also
    streams logs to the console if 'verbose' is set to True.

    Args:
        verbose (bool): If True, logs will also be printed to the console.
    """
    
    # --- Create Log Directory ---
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # --- Generate Timestamped Log Filename ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"agent_run_{timestamp}.log")

    # --- Get Logger Instance ---
    # We use a named logger so we can access this exact logger
    # configuration from other modules (like main.py and call_function.py)
    # by calling logging.getLogger("agent_logger").
    logger = logging.getLogger("agent_logger")
    logger.setLevel(logging.INFO) # Set the minimum level to log.

    # --- Create Formatter ---
    # Define the format for all log messages.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # --- Configure File Handler (Always on) ---
    # This handler writes all INFO-level (and higher) logs to the timestamped file.
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- Configure Console Handler (Optional) ---
    # This handler streams logs to the console (sys.stderr)
    # only if the verbose flag was passed.
    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # --- Prevent duplicate logging (if setup is called multiple times) ---
    # This ensures we don't add handlers repeatedly if the function
    # were ever to be called more than once.
    logger.propagate = False