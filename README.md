# Bikepoint-ELT

This is a project using the Bikepoint API (https://api-portal.tfl.gov.uk/api-details#api=BikePoint&operation=BikePoint_GetAll) to practice the ELT process.

The aim of this project is to code a modular ELT process in python which can be used to monitor and investigate which bike points experience higher / lower demand at different times of day. This can be used to help TFL in their planning for where to build effective new bike points, as well as help them in the day to day management if they need to send vans to move bikes from full bikepoints to empty ones.

---

## Extract Stage

The first stage of this ELT process is the extraction stage. Its purpose is to collect raw bike point data from the TfL Bikepoint API and store it safely for later processing.

### What happens in this stage?

#### 1. Creating a timestamped output

A timestamp is created for each run so that output files are uniquely named.

```python
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{data_dir}/{timestamp}.json'
```

#### 2. Setting up logging

A log file is set up to record the process and any errors.

```python
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

#### 3. Creating folders for storage

A folder is created to store the extracted JSON data and log files.

```python
log_dir = 'logs'
data_dir = 'data'
os.makedirs(log_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)
```

#### 4. Sending the API request

The script sends a request to the Bikepoint API.

```python
response = requests.get(url)
status = response.status_code
```

#### 5. Saving successful responses

If the request is successful, the response data is saved as a JSON file.

```python
if 200 <= status < 300:
    data = response.json()
    with open(filename, 'w') as file:
        json.dump(data, file)
```

#### 6. Handling failures and retries

If the request fails or returns no data, the script logs the issue and retries a limited number of times.

```python
while attempt < max_retry:
    response = requests.get(url)
    status = response.status_code

    if 200 <= status < 300:
        data = response.json()
        if len(data) > 0:
            break
    elif status <= 100 or status >= 500:
        time.sleep(delay)
        attempt += 1
```

### Why this stage is important

This stage ensures that the raw data is captured consistently and can be used later for analysis. It also makes it easier to troubleshoot problems by logging each stage of the ingestion, helping to pinpoint if anything has gone wrong in the process.
