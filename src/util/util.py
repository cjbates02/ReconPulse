import logging
import subprocess

def get_logger(name, write_file=False):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if write_file:
            file_handler = logging.FileHandler('app.log', mode='a')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

logger = get_logger(__name__)

def execute_subprocess_command(command):
    command = command.split(' ')
    try:
        output = subprocess.check_output(command, text=True)
        return output
    except subprocess.CalledProcessError as e:
        logger.error(f'Failed to execute command: {command}. Exit code: {e.returncode}.')