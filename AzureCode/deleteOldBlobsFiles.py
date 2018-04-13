from azure.storage.blob import BlockBlobService, PublicAccess


def main():
    # Create the BlockBlockService that is used to call the Blob service for
    # the storage account
    block_blob_service = BlockBlobService(
        account_name='optiondatastorage',
        account_key='X6s7Fmxhb6TM/+OhvIl0rNHhOQebO701I1dVdzaW6pKvdi9uVKFgRyW771hrvfCf1TgRA9v+5D7p76pw9ROR6g==')
    container_name = 'sparkoptions-2018-04-02t11-05-13-262z'
    # Set the permission so the blobs are public
    block_blob_service.set_container_acl(
        container_name, public_access=PublicAccess.Container)

    blobs = block_blob_service.list_blobs(container_name)

    for i in blobs:
        if "GPUData/" in i.name:  # check for certain folder (GPUData folder)
            block_blob_service.delete_blob(
                container_name, i.name)  # delete all blobs in that folder


# Stops code being run on import
if __name__ == "__main__":
    main()
