import socket
import json
from server.core.utils import login_check
import os


class Server(object):
    def __init__(self, ip, port):
        self.server = socket.socket()
        self.server.bind((ip, port))
        self.server.listen(5)
        self.path = ''


    def connect(self):
        self.conn, self.addr = self.server.accept()
        print('客户端{}已连接'.format(self.addr))


    def _recv(self):
        data = self.conn.recv(1024)
        data = str(data, encoding='utf8')
        data = json.loads(data)
        return data

    def _send(self, data):
        data = bytes(json.dumps(data), encoding='utf8')
        self.conn.send(data)

    def login(self):
        userinfo = self._recv()
        username = userinfo.get('username')
        password = userinfo.get('password')
        print('username: {}\n password: {}'.format(username, password))
        res = login_check(username, password)
        print(res)
        self._send(res)
        return res


    def handler(self):
        cmd = self._recv()
        cmd_head = cmd.get('cmd_head')
        cmd.pop('cmd_head')
        if hasattr(self, cmd_head):
            func = getattr(self, cmd_head)
            func(list(cmd.values())[0])


    def cd(self, path):
        print(self.path.split('/'))
        if path == '..':
            if len(self.path.split('/')) == 2:
                res = {
                    'code': 403,
                    'msg': '无权限进入根目录'
                }
            else:
                res = {
                    'code': 200
                }
                self.path = '/'.join(self.path.split('/')[0:-1])
            self._send(res)
        else:
            path = self.path + '/' + path
            if os.path.isdir(path):
                res = {'code': 200}
            else:
                res = {
                    'code': 400,
                    'msg': '路径不存在!'
                }
            self._send(res)
            self.path = path
