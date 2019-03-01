import socket
import json


class Client(object):
    def __init__(self, ip, port):
        self.client = socket.socket()
        self.client.connect((ip, port))
        self.path = ''


    def _send(self, data):
        data = bytes(json.dumps(data), encoding='utf8')
        self.client.send(data)

    def _recv(self):
        data = self.client.recv(1024)
        data = str(data, encoding='utf8')
        data = json.loads(data)
        return data

    def login(self):
        username = input('>>请输入用户名：').strip()
        password = input('>>请输入密码：').strip()
        userinfo = {'username': username,
                    'password': password
                    }
        self._send(userinfo)
        data = self._recv()
        print(data)
        return data


    def interactive(self):
        cmd = input(self.path + '>>' ).split(' ')
        cmd_head = cmd[0]
        print(cmd, cmd_head)
        if hasattr(self, cmd_head):
            func = getattr(self, cmd_head)
            func(cmd[1])


    def cd(self, path):
        data = {
            'cmd_head': 'cd',
            'path': path
        }
        self._send(data)
        res = self._recv()

        if res.get('code') == 200:
            if path == '..':
                self.path = '/'.join(self.path.split('/')[0:-1])
            else:
                self.path = self.path + '/' + path
        else:
            print(res.get('msg'))



