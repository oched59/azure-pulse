import datetime
import logging
import os
import feedparser

import azure.functions as func

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


    # Fetch the RSS feed
    feed_url = "http://azure.microsoft.com/en-us/updates/feed/"

    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        logging.error('Error fetching RSS feed: %s', e)
        return


    # Set up Azure Blob Storage
    connection_string = os.getenv("AzureWebJobsStorage")

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_container_client = blob_service_client.get_container_client("rawdata")

    except Exception as e:
        logging.error('Error setting up Blob Storage: %s', e)
        return

    # Set up Azure Queue Storage
    try:
        queue_service_client = QueueServiceClient.from_connection_string(connection_string)
        queue_client = queue_service_client.get_queue_client("rawstoragequeue")
    except Exception as e:
        logging.error('Error setting up Queue Storage: %s', e)
        return

    # Process each entry in the feed
    for entry in feed.entries:
        # Construct a filename for the blob
        blob_name = f"update_{utc_timestamp}_{entry.title}.xml"

        try:
            # Save the entry to Blob Storage
            blob_client = blob_container_client.get_blob_client(blob_name)
            blob_client.upload_blob(entry.content[0].value)
        except Exception as e:
            logging.error('Error saving blob: %s', e)
            continue

        try:
            # Add a message to the queue
            queue_client.send_message(blob_name)
        except Exception as e:
            logging.error('Error sending message to queue: %s', e)
            continue

    logging.info('Done processing feed.')