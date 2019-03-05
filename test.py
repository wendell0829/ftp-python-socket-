import os

# 列出该目录下所有文件和文件夹，返回一个list
# a = os.path.abspath('.')
# print(a)
#
# b = os.listdir('D:/python programs/ftp')
# print(b)

# os.mkdir('test')


# filepath = 'client/files/aa.mp3'
#
# with open(filepath, 'rb') as f:
#     line1 = f.readline()
#     print(line1)
#     line2 = line1.decode(encoding='')
#     print(line2)
#     line3 = bytes(line2, encoding='utf8')
#     print(line3)
#     print(line1==line3)
# import json
# a = {'sdaf': 'sdafsd'}
#
# b = json.dumps(a)
#
# print(b, type(b))
#
# import hashlib
#
# m = hashlib.md5()
#
# print(m.hexdigest())
#
# m.update(b'wqe')
#
# print(m.hexdigest())
#
# m.update(b'ss')
#
# print(m.hexdigest())
#
# m3 = hashlib.md5(b'wqess')
#
# print(m3.hexdigest())

print(os.path.getsize('client/files/aa.mp3'))





print(bytes(3518044))