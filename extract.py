import requests, os, json, logging, time
from datetime import datetime

url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True) # creates a folder called 'data' - if it already exists then it's ok - i.e. doesnt show an error
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # based on the date time now i.e. when it is extracted
filename = f'{data_dir}/{timestamp}.json' # filename based on timestamp
max_retry = 5
attempt = 0
delay = 10

response = requests.get(url)
data = response.json()

with open(filename, 'w') as file:
    json.dump(data, file)