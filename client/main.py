from client.client_socket import Client

LOGIN_SIANAL = 0
c = Client(ip='localhost', port=9999)
while not LOGIN_SIANAL:
    data = c.login()
    if data.get('code') == 200:
        LOGIN_SIANAL = True
        c.path = 'files/' + data.get('username')

while True:
    c.interactive()
