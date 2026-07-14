import requests, os, json, logging, time
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # based on the date time now i.e. when it is extracted
logger = logging.getLogger()
url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'

def extract_api(url, data_dir, timestamp, max_retry=3, delay=10):

    logger.info(f'Extract Stage initiated')

    # Making data directory if it doesn't already exist.
    os.makedirs(data_dir, exist_ok=True)
    filename = f'{data_dir}/{timestamp}.json' # creating a filename based on timestamp
    attempt = 0

    # Loop to call API and handle errors:

    while attempt < max_retry:
        response = requests.get(url)
        status = response.status_code
        if 200 <= status < 300:
            data = response.json()
            if len(data) > 0:          # Checking if the data delivered is NOT empty
                try:                   # Using a try / except incase there are errors writing to the file
                    with open(filename, 'w') as file:      # the 'w' means 'write' - alternative is 'r' - 'read'
                        json.dump(data, file)
                    logger.info('file loaded')
                    logger.info(f'File {filename} was successfully saved') # Adding info line to update log based on status of the response.
                except Exception as e:
                    logger.error(f'An error occurred: {e}')
                break
            else:
                logger.error('No data returned')
                break
        elif status <= 100 or status >=500:
            time.sleep(delay)
            logger.info('retrying')
            logger.info(f'Status code {status}. Retrying. This was attempt {attempt}') # Adding info line to update log based on status of the response.
            attempt += 1
        else:
            logger.error('fix something')
            logger.error(status)
            logger.error(f'Error. Status code {status}. Fix it') # Adding info line to update log based on status of the response.
            break
