import socket
import json
import os
import hashlib


class Client(object):
    def __init__(self, ip, port):
        self.client = socket.socket()
        self.client.connect((ip, port))
        self.path = ''


    def _send(self, data):
        if not isinstance(data, bytes):
            data = bytes(json.dumps(data), encoding='utf8')
        self.client.send(data)

    def _recv(self):
        data_raw = self.client.recv(1024)
        try:
            data = json.loads(str(data_raw, encoding='utf8'))
            if not isinstance(data, dict):
                data = data_raw
        except:
            data = data_raw
        return data

    def help(self, *args):
        print('''
            目前支持以下命令:
            help --------------------------- 获取命令提示
            ls   --------------------------- 显示当前路径下所有文件与文件夹
            cd (path) ---------------------- 移动到path路径, path为路径
            upload (filename) -------------- 上传文件（filename为文件名）， 文件必须在files文件夹下
            download(filename) ----------- 下载文件(filename为文件名)
        ''')

    def _login(self):
        username = input('>>请输入用户名：').strip()
        password = input('>>请输入密码：').strip()
        userinfo = {'username': username,
                    'password': password
                    }
        self._send(userinfo)
        data = self._recv()
        return data

    def _error(self):
        print('命令不存在或参数错误!')
        self.help()


    def interactive(self):
        cmd = input(self.path + '>>' ).lstrip().split(' ')
        cmd_head = cmd[0]
        if cmd_head[0] == '_':
            self._error()
        else:
            try:
                func = getattr(self, cmd_head)
                func(*cmd)
            except:
                self._error()


    def cd(self, *args):
        path = args[1]
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


    def ls(self, *args):
        data = {'cmd_head': 'ls'}
        self._send(data)
        dir_list = self._recv().get('data')
        for i in dir_list:
            print(i)


    def upload(self, *args):
        filename = args[1]
        filepath = 'files/'+ filename
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            fileinfo = {
                'cmd_head': 'upload',
                'filename': filename,
                'filesize': filesize
            }
            self._send(fileinfo)
            res = self._recv()
            if res.get('code') == 200:
                m = hashlib.md5()
                f = open(filepath, 'rb')
                while True:
                    sagment = f.readline()
                    if len(sagment) == 0: break
                    self._send(sagment)
                    m.update(sagment)
                f.close()
                md5_data = {
                    'md5': m.hexdigest()
                }
                self._send(md5_data)
                res = self._recv()
                print(res.get('msg'))
            else:
                print(res.get('msg'))
        else:
            print('文件不存在，请确认文件名是否正确')


    def download(self, *args):
        filename = args[1]
        filepath = 'files/' + filename
        if os.path.isfile(filepath):
            print('存储目录中已存在同名文件，请核验！')
        else:
            data = {
                'cmd_head': 'download',
                'filename': filename
            }
            self._send(data)
            res = self._recv()
            if res.get('code') == 200:
                filesize = res.get('filesize')
                filesize1 = res.get('filesize1')
                confirm = input('文件大小为 {} , 是否确认接收?(默认为yes, N for no)'.format(filesize1))
                if confirm != 'N':
                    data = {
                        'confirm': 'Y'
                    }
                    self._send(data)
                    m = hashlib.md5()
                    f = open(filepath, 'ab')
                    sagment_size = 0
                    while sagment_size < filesize:
                        sagment = self._recv()
                        f.write(sagment)
                        m.update(sagment)
                        sagment_size += len(sagment)
                    f.close()
                    data = {
                        'md5': m.hexdigest()
                    }
                    self._send(data)
                    print(self._recv().get('msg'))
            else:
                print(res.get('msg'))

