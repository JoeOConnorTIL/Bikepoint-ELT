from modules.logger import initiate_log
from modules.load import load
from modules.extract import extract_api
from datetime import datetime
from dotenv import load_dotenv
import os

# Setting variables
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'

# Start Log
logger = initiate_log(timestamp, log_dir)
logger.info('Logger successfully initiated')

# Setting API call variables, running function to save to local folder

url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'
extract_api(url, data_dir, timestamp, max_retry=3, delay=10)

# Set .env variables

load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Run the load function

load(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)