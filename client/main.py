from client.client_socket import Client

LOGIN_SIANAL = 0
c = Client(ip='localhost', port=9999)
while not LOGIN_SIANAL:
    data = c._login()
    if data.get('code') == 200:
        print('欢迎您, {}'.format(data.get('username')))
        LOGIN_SIANAL = True
        c.path = 'files/' + data.get('username')
    else:
        print(data.get('msg'))

while True:
    c.interactive()
