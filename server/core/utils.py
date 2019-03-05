from server.core.database import User, session


def add_user(username, password):
    user = User(username, password)
    session.add(user)
    session.commit()


def login_check(username, password):
    '''
    根据username在数据库中查找记录, 然后比对password
    :param username:
    :param password:
    :return:
    '''
    user = session.query(User).filter_by(username=username).one_or_none()
    if user:
        if user.check_password(password):
            return {
                'code': 200,
                'msg': '登录成功',
                'username' : username
            }
        else:
            return {
                'code': 400,
                'msg': '密码错误'
            }
    else:
        return {
                'code': 400,
                'msg': '用户不存在'
            }


def bytes_trans(bytes):
    if bytes < 1024:  #比特
        bytes = str(round(bytes, 2)) + ' B' #字节
    elif bytes >= 1024 and bytes < 1024 * 1024:
        bytes = str(round(bytes / 1024, 2)) + ' KB' #千字节
    elif bytes >= 1024 * 1024 and bytes < 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024, 2)) + ' MB' #兆字节
    elif bytes >= 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024, 2)) + ' GB' #千兆字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024, 2)) + ' TB' #太字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' PB' #拍字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024 /1024, 2)) + ' EB' #艾字节
    return bytes