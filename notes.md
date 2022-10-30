# Setup.py
Enables the registry of all the packages properly. Run it using 'python setup.py install' command. It will find out all packages from the present directory and install the required packages from requirements.txt file.

# Avnesh Yadav
https://github.com/avnyadav/sensor-fault-detection.git

# Set the env_variables


# Logger
- use from_root() function to fetch the current project root.
- set basic configuration:
    logging.baseConfig
    (
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    )   
