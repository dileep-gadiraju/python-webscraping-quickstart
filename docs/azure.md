# Azure

1. Initialize BlobStorage object.
```
blob_storage = BlobStorage()
```

2. Set the folder for storage.
```
blob_storage.set_agent_folder(folder_name)
```
arguments:
    
* folder_name : Name of the folder.


3. Upload it to BlobStorage.

```
b_status, b_str = blob_storage.upload_file(file_name, data, overwrite)
```
arguments:
    
* file_name : Name of the file.
* data : data to be uploaded.
* overwrite : (boolean), flag for overwriting the data to BlobStorage.

return:

* b_status : (boolean), if the data has uploaded or not.
* b_str : Exception if the data is not uploaded.
