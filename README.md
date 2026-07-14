# Bikepoint-ELT

This project uses the TfL Bikepoint API to practise building a simple ELT pipeline in Python. The aim is to collect live bike point data, store it safely, and prepare it for later analysis and reporting.

The pipeline is designed to help investigate patterns in bike availability across different locations and times of day. This could support TfL in planning where new bike points might be most useful or where bikes may need to be redistributed.

---

## What this project does

The project follows a basic ELT flow:

1. Extract data from the Bikepoint API
2. Save the raw JSON response to a timestamped local file
3. Create logs for traceability
4. Upload the extracted files to an S3 bucket
5. Remove the local copies once they have been uploaded

The code is split into small, reusable modules so the process is easier to understand and maintain.

### Main workflow

The main script is the entry point for the pipeline.

```python
from modules.logger import initiate_log
from modules.load import load
from modules.extract import extract_api

logger = initiate_log(timestamp, log_dir)
extract_api(url, data_dir, timestamp, max_retry=3, delay=10)
load(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)
```

This keeps the orchestration simple while the actual work is handled by separate functions.

---

## Repository folder map

```text
Bikepoint-ELT/
├── main.py
├── load_test.py
├── requirements.txt
├── README.md
├── data/                 # generated JSON files from extraction
├── logs/                 # generated log files
└── modules/
    ├── extract.py        # API extraction logic
    ├── load.py           # uploads data to S3
    └── logger.py         # logging setup
```

---

## Script flow

```text
+-------------------+
| main.py           |
| orchestrates flow |
+--------+----------+
         |
         v
+-------------------+
| modules/logger.py |
| start logging     |
+--------+----------+
         |
         v
+-------------------+
| modules/extract.py|
| call Bikepoint API|
| save JSON file    |
+--------+----------+
         |
         v
+-------------------+
| data/             |
| timestamped files |
+--------+----------+
         |
         v
+-------------------+
| modules/load.py   |
| upload to S3      |
| remove local file |
+--------+----------+
         |
         v
+-------------------+
| AWS S3 bucket     |
+-------------------+
```

---

## Extract stage

The extract stage is responsible for calling the TfL Bikepoint API and saving the response locally.

A key part of this stage is the retry logic, which helps handle temporary failures gracefully.

```python
while attempt < max_retry:
    response = requests.get(url)
    status = response.status_code

    if 200 <= status < 300:
        data = response.json()
        if len(data) > 0:
            with open(filename, 'w') as file:
                json.dump(data, file)
            break
    elif status <= 100 or status >= 500:
        time.sleep(delay)
        logger.info('retrying')
        logger.info(f'Status code {status}. Retrying. This was attempt {attempt}')
        attempt += 1
```

This shows that the script retries after a server-side or low-status response instead of giving up immediately.

This stage also creates a timestamped filename so each run is stored separately.

```python
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{data_dir}/{timestamp}.json'
```

---

## Load stage

Once a file has been extracted, the load stage uploads it to an AWS S3 bucket.

The current implementation:

- reads AWS credentials from a .env file
- creates an S3 client
- uploads each file in the data folder
- removes the local file after a successful upload

Here is the core upload logic:

```python
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

for file in files:
    to_upload = f'{data_dir}/{file}'
    s3_client.upload_file(to_upload, AWS_BUCKET_NAME, file)
    os.remove(to_upload)
```

This shows how the extracted JSON files are transferred into S3 and then cleaned up locally.

---

## Logging

Each run produces a log file in the logs folder. Logging is set up centrally in the logger module so that the whole pipeline can be tracked more clearly.

```python
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

A simple example of the logger being created and used looks like this:

```python
logger = initiate_log(timestamp, log_dir)
logger.info('Logger successfully initiated')
logger.info('Load Stage initiated')
```

This makes it easier to follow the pipeline and diagnose issues when a run fails.

---

## How to run

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Create a .env file with your AWS credentials:

```text
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
```

3. Run the main script:

```bash
python main.py
```

This will start the full process from extraction through to S3 upload.
