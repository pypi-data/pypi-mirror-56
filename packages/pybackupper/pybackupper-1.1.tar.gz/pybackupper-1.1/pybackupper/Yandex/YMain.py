import YAuth
import YRequests
import os
import sys


class Flow:
    def __init__(self, id, secret , overwrite='true'):
        auth_init = YAuth.Auth(id, secret)
        security_code = auth_init.get_code()
        access_token = auth_init.exchange_code(security_code)
        self.yandex_requests = YRequests.Yandex_Requests(access_token)
        self.overwrite = overwrite

    @staticmethod
    def get_link(parents, filename):
        return 'disk:/' + parents + filename

    def get_files(self):
        self.files = self.yandex_requests.get_files()
        for file in self.files:
            print(file)

    def upload_file(self, filename, parents=''):
        """
        Upload file with fielname on Yandex Disk
        parents format is
        folder/folder/folder/
        """
        name = os.path.basename(filename)
        if len(parents) > 0:
            parents += '/'
        if self.overwrite == 'false' and \
           Flow.get_link(parents, name) in self.files:
            print('File ', name, ' is already exist...')
            answer = ask_overwrite(name)
            if answer == 'false':
                i = 1
                while 1:
                    parts = name.rsplit('.', 1)
                    if i == 1:
                        name = parts[0] + '(1).' + parts[1]
                    else:
                        name = parts[0][:-(len(str(i)) + 1)]
                        + '{0}'.format(i) + ').' + parts[1]
                    if not Flow.get_link(parents, name) in self.files:
                        break
                    i += 1
        prepared_filepath = parents.replace('/', '%2F') + name
        link = self.yandex_requests.get_upload_url(prepared_filepath)
        return (self.yandex_requests.upload_file(filename, link), name)

    def create_folder(self, foldername, parents=''):
        """
        Create folder with foldername name
        parents format
        folder1/folder2/folder3
        """
        formatted_parents = (parents + '/').replace('/', '%2F')

        return self.yandex_requests.create_folder(
            foldername, formatted_parents)

    def upload_dir(self, dirpath, parents=''):
        """
        Upload directory which is stored
        in dirpath and put it in parents folders
        Parents format: folder1/folder2..../folder
        """
        dirname = dirpath.split('\\')[-1]
        status = self.create_folder(dirname, parents)
        if status == 201:
            print('[YaDisk]: Folder {0} is created!'
                  .format(parents + '/' + dirname))
        elif status == 409:
            print('[YaDisk]: Folder {0} is already exists...'
                  .format(parents + '/' + dirname))
        if len(parents) > 0:
            parents += '/'
        parents += dirname
        file_list = os.listdir(dirpath)
        for obj in file_list:
            name = dirpath + '\\' + obj
            if os.path.isfile(name):
                status = self.upload_file(name, parents)
                if status[0] == 201:
                    print('[YaDisk]: File {0} is successfully created'
                          .format(parents + '/' + status[1]))
            else:
                self.upload_dir(name, parents)


def ask_usage():
    print('Would you like to use Yandex Disk?')
    answer = input('Answer [y/n]: ')
    while not (answer.strip().lower() == 'y' or answer.strip().lower() == 'n'):
        print('Incorrect answer')
        print(answer)
        answer = input('Answer [y/n]: ')
    if answer == 'y':
        return 1
    else:
        return 0


def ask_overwrite(file='already existing files'):
    print('Would you like to overwrite {0}?'.format(file))
    answer = input('Answer [y/n]: ')
    while not (answer.strip().lower() == 'y' or answer.strip().lower() == 'n'):
        print('Incorrect answer')
        print(answer)
        answer = input('Answer [y/n]: ')
    if answer == 'y':
        return 'true'
    else:
        return 'false'
