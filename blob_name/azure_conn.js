// npm install @azure/storage-blob
const { BlobServiceClient } = require("@azure/storage-blob");

// Connection string for your Azure Storage Account
const connectionString = "<your_connection_string>";

// Name of the container
const containerName = "<your_container_name>";

// Create a blob service client
const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);

// Get the container client
const containerClient = blobServiceClient.getContainerClient(containerName);

// List all blobs in the container and print their names
async function listBlobs() {
    let iter = containerClient.listBlobsFlat();
    for await (const blob of iter) {
        console.log(blob.name);
    }
}

listBlobs().catch(console.error);
