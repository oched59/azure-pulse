import datetime
import json
import logging
import os
import ssl
import urllib.parse
import feedparser
import requests
from datetime import datetime, timedelta, timezone

import azure.functions as func

import xml.etree.ElementTree as ET

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient
import urllib3

#os.environ['REQUESTS_CA_BUNDLE'] = 'certs/storage_cert.crt'

app = func.FunctionApp()

@app.schedule(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def CrawlerTimerTrigger(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=timezone.utc).isoformat()

    if myTimer.past_due:
        logging.info('The timer is past due!')

#    return
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    # Fetch the RSS feed
    feed_url = "http://azure.microsoft.com/en-us/updates/feed/"
    print(" Inside")
     
    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        logging.error('Error fetching RSS feed: %s', e)
        return

    # Set up Azure Blob Storage
    connection_string = os.getenv("AzureWebJobsStorage")
    print(connection_string)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_container_client = blob_service_client.get_container_client("rawdata")

    except Exception as e:
        logging.error('Error setting up Blob Storage: %s', e)
        return

    # Set up Azure Crawler Storage
    try:
        queue_service_client = QueueServiceClient.from_connection_string(connection_string)
        queue_client = queue_service_client.get_queue_client("webcrawlerqueue")
    except Exception as e:
        logging.error('Error setting up Queue Storage: %s', e)
        return
    
    # table_service_client = TableServiceClient.from_connection_string(connection_string)
    table_name = "metadata"
    table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)

    # get xml feeds to crawl
    entities, crawled = get_xml_feeds_due_for_crawling(table_client, table_name)

    for entity in entities:
        feed_url = entity['FullUrl']

        # Download the XML data from the feed URL and save to blob storage
        # response = requests.get(feed_url)
        # xml_data = response.content
        # try:
        #     # Save the entry to Blob Storage
        #     last_file = f"master/xml/{utc_timestamp}_azure_update_feed.xml"
        #     blob_client = blob_container_client.get_blob_client(last_file)
        #     blob_client.upload_blob(xml_data)
        # except Exception as e:
        #     logging.error('Error saving blob: %s', e)

        # Process each entry in the feed
        for entry in feed.entries:
            # construct metadata json
            item_data = create_item_data(entry)
        
            # Check if the entity already exists in the table
            try:
                entity = table_client.get_entity(item_data['PartitionKey'], item_data['RowKey'])
            except:
                entity = None

            if entity is None:
                # The entity does not exist, so add it to the table
                table_client.create_entity(entity=item_data)

                # Send the item data to the web crawler storage queue
                queue_client.send_message(json.dumps(item_data))
            elif is_due_for_crawling(entity):
                # The entity exists and is due for crawling, so update the LastCrawled attribute
                entity['LastCrawled'] = datetime.utcnow().isoformat() + 'Z'
                table_client.update_entity(table_name, entity)


        logging.info('Done processing feed.')

def get_xml_feeds_due_for_crawling(table_client, table_name):
    # Get the current date and time
    now = datetime.utcnow()

    # Calculate the date and time one day ago
    one_day_ago = now - timedelta(days=1)

    # Convert to ISO 8601 format
    one_day_ago_iso = one_day_ago.isoformat() + 'Z'  # Add 'Z' to indicate UTC
    crawled = now.isoformat() + 'Z'

    # Filter entities where ContentType is 'XML Feed' and LastCrawled is earlier than one day ago
    filter_string = f"ContentType eq 'XMLFeed' and LastCrawled lt '{one_day_ago_iso}'"
    entities = table_client.query_entities(filter_string)

    return entities, crawled

def create_item_data(item):
    # Extract the domain and path from the item URL
    url_parts = urllib.parse.urlparse(item.link)
    domain = url_parts.netloc
    path = urllib.parse.quote(url_parts.path, safe='')

    # Create a JSON object for the item
    item_data = {
        'PartitionKey': domain,
        'RowKey': path,
        'FullUrl': item.link,
        'LastCrawled': '0000-00-00T00:00:00Z',
        'LastIndexed': '0000-00-00T00:00:00Z',
        'Depth': 2,
        'Status': 'Init',
        'ContentType': 'WebPage',
        'Id': item.id,
        'Title': item.title,
        'Published': item.published
    }

    return item_data

def is_due_for_crawling(entity):
    # Parse the LastCrawled date as a datetime object
    last_crawled = datetime.fromisoformat(entity['LastCrawled'].rstrip('Z'))

    # Get the current date and time
    now = datetime.utcnow()

    # Calculate the time difference
    difference = now - last_crawled

    # Check if the difference is more than 24 hours
    return difference > timedelta(days=7)



#  ## Started new Azure function to crawl webpages based on "webcrawlerqueue" which have been put there from the FeedCrawler
# @app.queue_trigger(arg_name="azqueue", queue_name="webcrawlerqueue",
#                                connection="AzureWebJobsStorage")    
# def QueueWebCrawler(azqueue: func.QueueMessage):

#     # TO BE IMPLEMENTED
#     logging.info('Python Queue trigger processed a message: %s',
#                 azqueue.get_body().decode('utf-8'))

# ################################## Khushboo starts here ##################################

# @app.function_name(name="QueueFunc")
# @app.queue_trigger(arg_name="msg", queue_name="inputqueue",
# #                    connection="storageAccountConnectionString")  # Queue trigger
# @app.write_queue(arg_name="outputQueueItem", queue_name="outqueue",
#                  connection="storageAccountConnectionString")  # Queue output binding
# def test_function(msg: func.QueueMessage,
#                   outputQueueItem: func.Out[str]) -> None:
#     logging.info('Python queue trigger function processed a queue item: %s',
#                  msg.get_body().decode('utf-8'))
#     outputQueueItem.set('hello')


# @app.queue_trigger(arg_name="azqueue", queue_name="webcrawlerqueue",
#                                connection="AzureWebJobsStorage")            # Queue trigger
# # @app.write_queue(arg_name="outputQueueItem", queue_name="cleanstoragequeue",
# #                                connection="AzureWebJobsStorage")            # Queue output binding
# def test_function(msg: func.QueueMessage,
#                   outputQueueItem: func.Out[str]) -> None:
#     logging.info('Python queue trigger function processed a queue item: %s',
#                  msg.get_body().decode('utf-8'))
#     outputQueueItem.set('hello')





def queue_trigger_cleaner(azqueue: func.QueueMessage):
     logging.info('Python Queue trigger processed a message: %s',
                 azqueue.get_body().decode('utf-8'))



def parse_data_in_queue(msg: func.QueueMessage) -> None:
    # Retrieve the message content from the queue
    xml_file_path = msg.get_body().decode('utf-8')
    
    try:
        # Open and parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Convert XML to JSON
        json_data = {}
        parse_element(root, json_data)
        
        # Save the JSON data to a file
        json_file_path = xml_file_path.replace('.xml', '.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        print(f'Successfully converted {xml_file_path} to {json_file_path}')
    except Exception as e:
        print(f'Error converting {xml_file_path}: {str(e)}')

def parse_element(element, parent_json):
    # Convert XML element to JSON
    if element:
        if len(element) == 0:
            parent_json[element.tag] = element.text
        else:
            child_json = {}
            for child_element in element:
                parse_element(child_element, child_json)
            parent_json[element.tag] = child_json
    else:
        parent_json[element.tag] = element.text