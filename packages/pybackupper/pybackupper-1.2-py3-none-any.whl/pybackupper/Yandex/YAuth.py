import socket
import webbrowser
import requests
import json
import base64


class Auth:
    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        """
        Init Yandex Auth Class
        """
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET

    def get_code(self):
        """
        Get yandex security code,
        Which you later can exchange for
        Access token
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_OOBINLINE, 1)
        server.bind(('localhost', 5000))
        server.listen(1)

        link = 'https://oauth.yandex.ru/authorize'
        params = '?response_type=code&client_id={0}'.format(self.CLIENT_ID)
        webbrowser.open(link + params)

        link = ""
        while 'code' not in link:
            client, addr = server.accept()
            request = client.recv(1024)
            link = request.decode('utf-8').split('\r\n', 1)[0].split(' ')[1]
            client.sendall('Authorization complete!'.encode())
            client.close()
        link = link.split('&')[0]
        code = link[link.find('=') + 1:]
        server.close()
        return code

    def exchange_code(self, code):
        """
        Send a POST request and
        Change your security code to
        Access token
        """
        query_link = 'https://oauth.yandex.ru/token'
        secret_string = '{0}:{1}'.format(self.CLIENT_ID, self.CLIENT_SECRET)
        access = base64.b64encode(secret_string.encode())
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Authorization": "Basic " + str(access, 'utf-8')}
        data = {"grant_type": "authorization_code",
                "code": code}
        response = requests.post(query_link, headers=headers, data=data)
        if response.status_code != 200:
            raise ConnectionError
        return response.json()['access_token']
