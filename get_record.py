import os
import json
from azure.cosmos import CosmosClient, exceptions
from azure.storage.blob import BlobServiceClient

# Environment variables
COSMOS_URL = os.environ['COSMOS_URL']
COSMOS_KEY = os.environ['COSMOS_KEY']
COSMOS_DB_NAME = os.environ['COSMOS_DB_NAME']
COSMOS_CONTAINER_NAME = os.environ['COSMOS_CONTAINER_NAME']
BLOB_CONN_STR = os.environ['BLOB_CONN_STR']
BLOB_CONTAINER_NAME = os.environ['BLOB_CONTAINER_NAME']

# Initialize Cosmos DB client
cosmos_client = CosmosClient(COSMOS_URL, COSMOS_KEY)
db = cosmos_client.get_database_client(COSMOS_DB_NAME)
cosmos_container = db.get_container_client(COSMOS_CONTAINER_NAME)

# Initialize Blob client
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER_NAME)

def get_billing_record(record_id, partition_key):
    try:
        # Try fetching from Cosmos DB
        record = cosmos_container.read_item(item=record_id, partition_key=partition_key)
        return record
    except exceptions.CosmosResourceNotFoundError:
        try:
            # Fallback to Blob Storage
            blob_client = blob_container.get_blob_client(f"{record_id}.json")
            blob_data = blob_client.download_blob().readall()
            return json.loads(blob_data)
        except Exception as e:
            return {"error": f"Record not found in Cosmos DB or Blob: {str(e)}"}
