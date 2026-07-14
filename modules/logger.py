import os, logging

def initiate_log(timestamp:str, log_dir:str):
    """
    This initialises the logger for everything

    Args:
        timestamp(str): For the filenames of the logs.
        log_dir(str): Where the logs should be stored.
    """
    #timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # based on the date time now i.e. when it is extracted
    #log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True) # creates a folder called 'logs' - if it already exists then it's ok - i.e. doesnt show an error or do anything.
    log_filename = f'{log_dir}/bike_point_{timestamp}.log' # creating a string for the filename based on the timestamp

    # Configutring logging - anything INFO level and higher will be included
    logging.basicConfig(
        filename = log_filename,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level = logging.INFO
    )

    # Assign the logger
    return logging.getLogger()
    # logger.info('Logger successfully initiated')