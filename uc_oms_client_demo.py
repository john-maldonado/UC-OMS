import socket
import select
import errno
import sys
import json
from uc_oms_protocol import Protocol, PCommands, PExceptions

class OMSUser():
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = ''
        self.authenticated = False

username = input('Username: ')
password = input('Password: ')

u = OMSUser(username, password)

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
IP = "10.0.0.119"
PORT = 4444
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
client_socket.setblocking(False)

# Initiate Connection
p = Protocol()
p.sendConnect(client_socket)
client_socket.setblocking(True)
message = p.receiveMessage(client_socket)
client_socket.setblocking(False)
if message is False:
    print('Failed to connect to server')
else:
    command = message.command
    if command == PCommands.connect:
        print('Connected to server!')
    
    while True:
        print('1) Login')
        print('2) Logout')
        print('3) Query')
        print('4) Exit')
        selection = input('Please enter your selection: ')
        selection = int(selection)
        if selection == 4:
            break
        elif selection == 1:
            if not u.authenticated:
                print('Requesting login')
                p.sendLogin(client_socket, u.username, u.password)
                client_socket.setblocking(True)
                message = p.receiveMessage(client_socket)
                client_socket.setblocking(False)
                if message.command == PCommands.authenticate:
                    token = message.token
                    print('Succesfully Authenticated!')
                    print('Token: {}'.format(token))
                    u.authenticated = True
                    u.token = token
            else:
                print('Already logged in')
        elif selection == 2:
            print('Requesting logout')
            p.sendLogout(client_socket, u.username, u.token)
            client_socket.setblocking(True)
            message = p.receiveMessage(client_socket)
            client_socket.setblocking(False)
            if message.command == PCommands.logout:
                u.token = ''
                u.authenticated = False
                print('Logged Out')
        elif selection == 3:
            print('Requesting query')
            query_string = input('Enter SQL Query: ')
            p.sendQuery(client_socket, u.username, u.token, query_string)
            client_socket.setblocking(True)
            message = p.receiveMessage(client_socket)
            client_socket.setblocking(False)
            if message.command == PCommands.sendResults:
                results = json.loads(message.args)
                results = [tuple(i) for i in results]
                print(results)
            elif message.command == PCommands.exception:
                exception = message.args
                print(PExceptions.exceptions_desc_dict[exception])
        else:
            print('Invalid selection')