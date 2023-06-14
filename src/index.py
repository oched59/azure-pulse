from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField, SearchFieldDataType


endpoint = "https://gptkb-oaxatpknic6wq.search.windows.net"
key = "JXX68Zf11uns1DSKp5ERp75Dt3uVoyo7borwPuYAjpAzSeAq7ik9"
index_name = "indexinghtml"

# Create a new SearchIndexClient
credential = AzureKeyCredential(key)
client = SearchIndexClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)

# Define the index
index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SimpleField(name="url", type=SearchFieldDataType.String),
        SimpleField(name="published", type=SearchFieldDataType.String),
        SimpleField(name="last_crawled", type=SearchFieldDataType.String),
    ]
)

# Create the index
client.create_index(index)
