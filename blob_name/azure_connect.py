# pip install azure-storage-blob
from azure.storage.blob import BlobServiceClient

# Connection string for your Azure Storage Account
connection_string = "<your_connection_string>"

# Name of the container
container_name = "<your_container_name>"

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the container and print their names
blobs_list = container_client.list_blobs()
for blob in blobs_list:
    print(blob.name)
