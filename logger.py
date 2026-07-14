import os, logging
from datetime import datetime

def initiate_log():

    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # based on the date time now i.e. when it is extracted
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True) # creates a folder called 'logs' - if it already exists then it's ok - i.e. doesnt show an error or do anything.
    log_filename = f'{log_dir}/bike_point_{timestamp}.log' # creating a string for the filename based on the timestamp

    # Configutring logging - anything INFO level and higher will be included
    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(levelname)s - %(message)s', 
        level = logging.INFO
    )

    # Assign the logger
    logger = logging.getLogger()
    logger.info('Logger successfully initiated')