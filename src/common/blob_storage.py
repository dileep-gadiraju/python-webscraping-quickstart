import os

import config
from azure.storage.blob import BlobServiceClient


class BlobStorage(object):
    def __init__(self,overwrite=False):
        self.blob_service_client = BlobServiceClient(
            account_url=config.BLOB_ACCOUNT_URL, credential=config.BLOB_SAS_TOKEN)
        self.root_folder = None
        self.overwrite = overwrite

    @property
    def root_folder(self):
        return self._root_folder

    @root_folder.setter
    def root_folder(self, rf):
        self._root_folder = rf

    @property
    def blob_service_client(self):
        return self._blob_service_client

    @blob_service_client.setter
    def blob_service_client(self, bsc):
        self._blob_service_client = bsc

    def set_agent_folder(self, agent_folder):
        self.root_folder = agent_folder

    def upload_file(self,file_name,file_contents):
        upload_file_path = os.path.join(self.root_folder,file_name)
        blob_client = self.blob_service_client.get_blob_client(container=config.CONTAINER_NAME,blob=upload_file_path)
        try:
            blob_client.upload_blob(file_contents,overwrite=self.overwrite)
        except Exception as e:
            return False,str(e)
        return True,'true'
