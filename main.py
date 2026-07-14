from logger import initiate_log
from load import load
from extract import extract_api
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'
# Start Log
logger = initiate_log(timestamp, log_dir)
logger.info('Logger successfully initiated')

# Make the API call, save to local folder
extract_api()

# Load from local folder to s3 bucket, delete from local once completed
load()