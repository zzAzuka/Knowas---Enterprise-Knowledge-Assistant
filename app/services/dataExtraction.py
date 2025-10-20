import os
import boto3
import logging

BUCKET_NAME = 'knowledge-assistant-data-lake-sibirassal'
DOWNLOAD_DIR = './filesFromBucket'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def extractedfFromS3(filename:str) -> str | None:
    s3_client =  boto3.client('s3')
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    local_path = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(local_path):
        logging.info(f"File '{filename}' already exists locally. Skipping download.")
        return local_path
    
    try:
        s3_client.download_file(BUCKET_NAME, filename, local_path)
        logging.info(f"Download completed for {filename}!")
        return local_path
    except Exception as e:
        logging.info(f"Unexpected error occurred while downloading {filename}!")