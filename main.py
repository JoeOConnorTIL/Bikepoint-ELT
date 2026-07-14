from logger import initiate_log
from load import load
from extract import extract_api
from datetime import datetime
from dotenv import load_dotenv
import os

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'
# Start Log
logger = initiate_log(timestamp, log_dir)
logger.info('Logger successfully initiated')

# Make the API call, save to local folder
url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'
extract_api(url, data_dir, timestamp, max_retry=3, delay=10)

# Load from local folder to s3 bucket, delete from local once completed
load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

load(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)