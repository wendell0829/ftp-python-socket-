from server.core.database import User, session


def add_user(username, password):
    user = User(username, password)
    session.add(user)
    session.commit()


def login_check(username, password):
    user = session.query(User).filter_by(username='wendell').one_or_none()
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
