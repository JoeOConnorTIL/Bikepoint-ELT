from logger import initiate_log
from load import load
from extract import extract_api

# Start Log
initiate_log()

# Make the API call, save to local folder
extract_api()

# Load from local folder to s3 bucket, delete from local once completed
load()