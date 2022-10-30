"""
logger script is created for defining how to print the various types of logs.
"""
import logging
import os
from datetime import datetime

from from_root import from_root 
# from_root allows you to define the absolute paths avoiding the file not found type of errors.

# set the name of log file. 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# from_root function gives you the path of root directory of the project.
logs_path = os.path.join(from_root(), "logs", LOG_FILE)

# makedirs will create the directory and the files
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

if __name__ == "__main__":
    print("First line")
    print(from_root())
