import logging
import requests
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueClient
import json

def main(mytimer: func.TimerRequest, outputQueue: func.Out[str]) -> None:
    logging.info('Python timer trigger function executed.')

    # URL for crawling
    url = "https://azure.microsoft.com/en-us/updates/feed"

    # Connection string for Azure Storage account
    connection_string = "DefaultEndpointsProtocol=https;AccountName=genaipocambg;AccountKey=oFBsa6bp3ga8wfoETOmnM+4grRoOftB5vV2y1mIvVQDsXxupV4gQyXXvSoFCHITfPSpWejFUABDm+AStEYlIUg==;EndpointSuffix=core.windows.net"

    # Create a blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Create a container for storing raw HTML
    container_name = "rawhtml"
    container_client = blob_service_client.get_container_client(container_name)
    
    try:
        container_client.create_container()
        logging.info(f'Container "{container_name}" created.')
    except Exception:
        logging.info(f'Container "{container_name}" already exists.')

    # Create a queue client
    queue_name = "cleanqueue"
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)
    
    try:
        queue_client.create_queue()
        logging.info(f'Queue "{queue_name}" created.')
    except Exception:
        logging.info(f'Queue "{queue_name}" already exists.')

    # Retrieve the current time
    crawl_time = func.timestamp()

    # Define the blob name
    blob_name = f"{url.replace('http://', '')}.html"

    # Create a blob client for the container
    blob_client = container_client.get_blob_client(blob_name)

    # Get the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Upload the HTML content to the blob
    blob_client.upload_blob(html_content, overwrite=True)

    # Create a message for the cleaning queue
    message = {
        "blob_name": blob_name,
        "crawl_time": crawl_time
    }
    message_json = json.dumps(message)

    # Send the message to the cleaning queue
    outputQueue.set(message_json)

    # Log the completion of the function
    logging.info(f"Message sent to queue: {message_json}")
    logging.info('Crawling, uploading, and queuing completed.')
