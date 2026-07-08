import requests, os, json, logging, time
from datetime import datetime


##################################### LOGGING #########################################

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # based on the date time now i.e. when it is extracted
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True) # creates a folder called 'logs' - if it already exists then it's ok - i.e. doesnt show an error or do anything.
log_filename = f'{log_dir}/{timestamp}.log' # creating a string for the filename based on the timestamp

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(levelname)s - %(message)s', 
    level = logging.INFO
)

# Assign the logger
logger = logging.getLogger()
logger.info('Logger successfully initiated')

#################################### API SETUP ########################################

# Setting up variables for API call

url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True) # creates a folder called 'data' - if it already exists then it's ok - i.e. doesnt show an error or do anything.
filename = f'{data_dir}/{timestamp}.json' # filename based on timestamp
max_retry = 5
attempt = 0
delay = 10

# Loop to call API and handle errors:

while attempt < max_retry:
    response = requests.get(url)
    status = response.status_code
    if 200 <= status < 300:
        data = response.json()
        with open(filename, 'w') as file:
            json.dump(data, file)
        print('file loaded')
        logger.info(f'File {filename} was successfully saved') # Adding info line to update log based on status of the response.
        break
    elif status <= 100 or status >=500:
        time.sleep(delay)
        print('retrying')
        logger.info(f'Status code {status}. Retrying. This was attempt {attempt}') # Adding info line to update log based on status of the response.
        attempt += 1
    else:
        print('fix something')
        print(status)
        logger.error(f'Error. Status code {status}. Fix it') # Adding info line to update log based on status of the response.
        break
