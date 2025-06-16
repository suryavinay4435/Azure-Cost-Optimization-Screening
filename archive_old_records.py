import os
import json
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

# Environment variables (set these in Azure Function App settings or local.settings.json)
COSMOS_URL = os.environ['COSMOS_URL']
COSMOS_KEY = os.environ['COSMOS_KEY']
COSMOS_DB_NAME = os.environ['COSMOS_DB_NAME']
COSMOS_CONTAINER_NAME = os.environ['COSMOS_CONTAINER_NAME']
BLOB_CONN_STR = os.environ['BLOB_CONN_STR']
BLOB_CONTAINER_NAME = os.environ['BLOB_CONTAINER_NAME']

# Time threshold for archival (in days)
THRESHOLD_DAYS = 90

# Cosmos DB setup
cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
db = cosmos_client.get_database_client(COSMOS_DB_NAME)
container = db.get_container_client(COSMOS_CONTAINER_NAME)

# Blob Storage setup
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER_NAME)

# Date threshold
threshold_date = datetime.utcnow() - timedelta(days=THRESHOLD_DAYS)

# Query for old records
query = "SELECT * FROM c WHERE c.timestamp < @date"
params = [
    {"name": "@date", "value": threshold_date.isoformat()}
]

# Archive and delete records
for item in container.query_items(query=query, parameters=params, enable_cross_partition_query=True):
    blob_name = f"{item['id']}.json"
    blob_container.upload_blob(blob_name, json.dumps(item), overwrite=True)
    container.delete_item(item=item['id'], partition_key=item['partitionKey'])
    print(f"Archived and deleted record: {item['id']}")
