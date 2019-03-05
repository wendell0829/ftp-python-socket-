import socket
import json
from server.core.utils import login_check, bytes_trans
import os
import hashlib


class Server(object):
    def __init__(self, ip, port):
        '''
        创建socket对象, 监听给定的地址,  初始化工作路径
        :param ip: IP地址
        :param port: 端口号
        '''
        self.server = socket.socket()
        self.server.bind((ip, port))
        self.server.listen(5)
        self.path = ''


    def connect(self):
        self.conn, self.addr = self.server.accept()
        print('客户端{}已连接'.format(self.addr))


    def _recv(self):
        '''
        接收数据函数, 客户端传来的数据有两种:
        1. 标准json数据
        2. 字节流(传输文件时)
        :return: 1. 字典
                2. 字节流
        '''
        data_raw = self.conn.recv(1024)
        try:
            data = json.loads(str(data_raw, encoding='utf8'))
            if not isinstance(data, dict):
                data = data_raw
        except:
            data = data_raw
        return data


    def _send(self, data):
        '''
        发送数据, 如果数据为字典格式, 先转换为json对象再编码
        :param data:
        :return:
        '''
        if isinstance(data, dict):
            data = bytes(json.dumps(data), encoding='utf8')
        self.conn.send(data)

    def _login(self):
        '''
        登录函数, 接收登录信息, 进行登录验证
        :return:
        '''
        userinfo = self._recv()
        username = userinfo.get('username')
        password = userinfo.get('password')
        print('username: {}\n password: {}'.format(username, password))
        res = login_check(username, password)
        print(res)
        self._send(res)
        return res


    def handler(self):
        '''
        接收命令后, 进行预处理, 获得命令关键字, 映射到对应函数中去
        命令合法性在客户端验证
        :return:
        '''
        cmd = self._recv()
        cmd_head = cmd.get('cmd_head')
        cmd.pop('cmd_head')
        if hasattr(self, cmd_head):
            func = getattr(self, cmd_head)
            func(*list(cmd.values()))



    def cd(self, *args):
        path = args[0]
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
                self.path = path
                res = {'code': 200}
            else:
                res = {
                    'code': 400,
                    'msg': '路径不存在!'
                }
            self._send(res)


    def ls(self, *args):

        dir_list = os.listdir(self.path)
        res = {
            'code': 200,
            'data': dir_list
        }
        self._send(res)


    def upload(self, *args):
        filename = args[0]
        filepath = self.path + '/' + filename
        filesize = args[1]
        if os.path.isfile(filepath):
            res = {
                'code': 400,
                'msg': '目标目录存在同名文件， 请核验'
            }
            self._send(res)
        else:
            res = {
                'code': 200,
            }
            self._send(res)
            m = hashlib.md5()
            f = open(filepath, 'ab')
            sagment_size = 0
            while sagment_size < filesize:
                sagment = self._recv()
                f.write(sagment)
                m.update(sagment)
                sagment_size += len(sagment)
            f.close()
            m0 = self._recv().get('md5')
            if m.hexdigest() == m0:
                print('文件上传完毕')
                data = {
                    'code': 200,
                    'msg': '文件上传成功！'
                }
            else:
                data = {
                    'code': 400,
                    'msg': '文件上传失败，请重试！'
                }
            self._send(data)


    def download(self, *args):
        filename = args[0]
        filepath = self.path + '/' + filename
        if os.path.isfile(filepath):
            filesize = os.path.getsize(filepath)
            filesize1 = bytes_trans(filesize)
            fileinfo = {
                'code': 200,
                'filesize': filesize,
                'filesize1': filesize1
            }
            self._send(fileinfo)
            if self._recv().get('confirm') == 'Y':
                f = open(filepath, 'rb')
                m = hashlib.md5()
                while True:
                    sagment = f.readline()
                    if len(sagment) == 0: break
                    self._send(sagment)
                    m.update(sagment)
                f.close()
                m0 = self._recv().get('md5')
                if m.hexdigest() == m0:
                    print('文件下载完毕')
                    data = {
                        'code': 200,
                        'msg': '文件下载成功！'
                    }
                else:
                    data = {
                        'code': 400,
                        'msg': '文件下载失败，请重试！'
                    }
                self._send(data)
        else:
            data = {
                'code': 400,
                'msg': '文件不存在!'
            }
            self._send(data)



