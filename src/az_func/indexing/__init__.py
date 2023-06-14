import logging
import azure.functions as func
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

def main(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a message.')

    # Get the connection string for your Azure Storage account
    connection_string = "DefaultEndpointsProtocol=https;AccountName=genaipocambg;AccountKey=oFBsa6bp3ga8wfoETOmnM+4grRoOftB5vV2y1mIvVQDsXxupV4gQyXXvSoFCHITfPSpWejFUABDm+AStEYlIUg==;EndpointSuffix=core.windows.net"
    
    # Create a blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the message content
    message = msg.get_body().decode('utf-8')

    # Assuming the message contains the URL of the blob
    blob_url = message

    # Get the blob client
    #blob_client = blob_service_client.get_blob_client(blob_url)

    # Download the blob content
    #html_content = blob_client.download_blob().content_as_text()
    # Extract the blob name from the URL
    blob_name = blob_url.split("/")[-1]

    # Get the blob client
    blob_client = blob_service_client.get_blob_client(container="rawhtml", blob=blob_name)

    # Download the blob content
    html_content = blob_client.download_blob().content_as_text()


    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all items in the RSS feed
    items = soup.find_all('item')

    # Define the endpoint and api-key for your search service
    endpoint = "https://gptkb-oaxatpknic6wq.search.windows.net"
    key = "JXX68Zf11uns1DSKp5ERp75Dt3uVoyo7borwPuYAjpAzSeAq7ik9"
    


    # Create a SearchClient
    credential = AzureKeyCredential(key)
    client = SearchClient(endpoint=endpoint,
                          index_name="indexinghtml",
                          credential=credential)

    # Get the current time
    crawl_time = datetime.utcnow()

    # For each item, extract the title, link, description, and last update time, and add them to the index
    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text
        last_update_time = parse(item.find('pubdate').text)

        # Create a document
        document = {
            "id": link, 
            "title": title,
            "link": link,
            "description": description,
            "last_update_time": last_update_time,
            "crawl_time": crawl_time
        }

        # Upload the document to the index
        client.upload_documents(documents=[document])

    logging.info('Processing and indexing completed.')
