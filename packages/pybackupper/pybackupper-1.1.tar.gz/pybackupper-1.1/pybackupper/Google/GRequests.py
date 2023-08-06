import requests
import json


class Requests:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_files(self):
        """
        Get All Files from your Google Drive
        Output: [ (string id, string filename) ]
        """
        result = []
        headers = {"Authorization": "Bearer " + self.access_token}
        query_link = 'https://www.googleapis.com/drive/v3/files'
        query_params = "?pageSize=1000"
        url = '{0}{1}'.format(query_link, query_params)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ConnectionError
        content = response.json()
        for file in content['files']:
            result.append((file['id'], file['name']))
        return result

    def upload_file(self, filename, filepath, parentID):
        """
        Upload file on Your Google Drive
        Filename: "example.jpg"
        Filepath: ".../.../"
        ParentID: "ID of folder, where file should be placed"
        Output: string ID of created file
        """
        query_link = 'https://www.googleapis.com/upload/drive/v3/files'
        query_params = "?uploadType=multipart"
        link = '{0}{1}'.format(query_link, query_params)
        headers = {"Authorization": "Bearer " + self.access_token}
        meta_data = {
            "name": filename,
            "parents": [parentID]
        }
        files = {
            "data": ("metadata", json.dumps(meta_data, ensure_ascii=False),
                     "application/json; charset=UTF-8"),
            "file": open(filepath + '\\' + filename, 'rb')}
        response = requests.post(link, headers=headers, files=files)
        id = response.json()['id']
        print('[GDrive]: File {0} successfully uploaded! ID {1}'
              .format(filename, id))
        return id

    def create_folder(self, foldername, parentID):
        """
        Creater folder on Your Google Drive
        Foldername: name of folder
        ParentID: "ID of folder, where folder should be created"
        Output: string ID of created file
        """
        query_link = 'https://www.googleapis.com/upload/drive/v3/files'
        query_params = "?uploadType=multipart"
        link = '{0}{1}'.format(query_link, query_params)
        headers = {"Authorization": "Bearer " + self.access_token}
        meta_data = {
            "name": foldername,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parentID]
        }
        files = {"data": ("metadata", json.dumps(meta_data),
                          "application/json; charset=UTF-8")}
        response = requests.post(link, headers=headers, files=files)
        if response.status_code != 200:
            raise ConnectionError
        id = response.json()['id']
        print('[GDrive]: Folder {0} successfully created! ID {1}'
              .format(foldername, id))
        return id
