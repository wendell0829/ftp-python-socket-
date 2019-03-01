from server.core.server_socket import Server


LOGIN_SIGNAL = False
s = Server(ip='localhost', port=9999)
s.connect()
while not LOGIN_SIGNAL:
    res = s.login()
    if res.get('code') == 200:
        LOGIN_SIGNAL = True
        s.path = 'files/' + res.get('username')


while True:
    s.handler()