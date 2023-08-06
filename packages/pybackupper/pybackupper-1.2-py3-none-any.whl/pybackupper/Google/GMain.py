import GAuth
import GRequests
import os

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'google_client_secret.json'
APPLICATION_NAME = 'BackUpper'


class Flow:
    def __init__(self):
        auth_init = GAuth.Auth(
            SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
        credentials = auth_init.get_credentials()
        self.google_requests = GRequests.Requests(
            credentials.access_token)

    def get_files(self):
        """
        Get All Files from your Google Drive
        Output: [ (string id, string filename) ]
        """
        return self.google_requests.get_files()

    def upload_file(self, filename, parent_id='root'):
        """
        Upload file on Your Google Drive
        Filename: Full filename ("../..../example.jpg")
        parent_id: "ID of folder, where file should be placed"
        Output: string ID of created file
        """
        return self.google_requests.upload_file(
            os.path.basename(filename), os.path.dirname(filename), parent_id)

    def create_folder(self, foldername, parent_id='root'):
        """
        Creater folder on Your Google Drive
        Foldername: name of folder
        parent_id: "ID of folder, where folder should be created"
        Output: string ID of created file
        """
        return self.google_requests.create_folder(foldername, parent_id)

    def upload_dir(self, dirpath, parent_id='root'):
        """
        Upload directory on Your Google Drive
        Dirpath: full directory path
        parent_id: "ID of folder, where file should be placed"
        Output: string ID of created file
        """
        dirname = dirpath.split('\\')[-1]
        id = self.create_folder(dirname, parent_id)
        file_list = os.listdir(dirpath)
        for file in file_list:
            filename = dirpath + '\\' + file
            if os.path.isfile(filename):
                self.upload_file(filename, id)
            else:
                self.upload_dir(filename, id)


def ask_usage():
    print('Would you like to use Google Drive?')
    answer = input('Answer [y/n]: ')
    while not (answer.strip().lower() == 'y' or answer.strip().lower() == 'n'):
        print('Incorrect answer')
        print(answer)
        answer = input('Answer [y/n]: ')
    if answer == 'y':
        return 1
    else:
        return 0
