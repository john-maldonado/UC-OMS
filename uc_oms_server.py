# Import Libraries
import socket
import select
import secrets
import json
from passlib.context import CryptContext

# Import UC OMS Libraries
from uc_oms_protocol import Protocol, PCommands, PMessage, PExceptions, PObject, OMSUser
from uc_oms_db_connections import loginDBConnect, ordersDBConnect
from uc_oms_db_queries import (
    query_selectUsernameAndPasswordByUsername, 
    query_selectAllOpen
    )

# Set password encryption context
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
    )

# Create empty dictionary of valid tokens
valid_tokens = {}

# Create protocol instance
p = Protocol()

# Define listening address and port
IP = "0.0.0.0"
PORT = 4444
# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind port and listen
server_socket.bind((IP, PORT))
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

while True:

     # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Recieve message
            message = p.receiveMessage(client_socket)

            # If False - client disconnected before he sent his name
            if message is False:
                continue
            else:
                command = message.command
                # Check if message was a connect message
                if command == PCommands.connect:
                    # Add accepted socket to select.select() list
                    sockets_list.append(client_socket)
                    clients[client_socket] = client_address
                    p.sendConnect(client_socket)
                    print('Accepted new connection from {}:{}'.format(*client_address))
                else:
                    print('Invalid request from {}:{}'.format(*client_address))
                    p.sendException(notified_socket, PExceptions.invalid_request)
        
        # Else existing socket is sending a message
        else:
            # Receive message
            message = p.receiveMessage(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue
            # Else, process the command
            else:
                command = message.command
                # Handle Login
                if command == PCommands.login:
                    user = message.user
                    password = message.args
                    print('Processing login for: {} Identified by: {}'.format(user, password))
                    # Pull hashed password from DB
                    db_connection = loginDBConnect()
                    result = query_selectUsernameAndPasswordByUsername(db_connection, user)
                    authenticated = False
                    # Check if 1 result is returned
                    if len(result) == 1:
                        password_result = result[0][1]
                        # Check if password matches hashed password
                        if pwd_context.verify(password, password_result):
                            authenticated = True
                    if authenticated:
                        # Send token to client
                        print('Password OK')
                        print('Sending token to client')
                        token = secrets.token_urlsafe()
                        valid_tokens.update({token : user})
                        p.sendAuthenticate(notified_socket, token)
                    else:
                        p.sendException(notified_socket, PExceptions.invalid_credentials)
                # Handle Logout
                elif command == PCommands.logout:
                    user = message.user
                    token = message.token
                    print('Processing logout for: {} Identified by: {}'.format(user, token))
                    if token in valid_tokens:
                        del valid_tokens[token]
                    p.sendLogout(notified_socket, OMSUser(user, ''))
                # Handle Select Queries
                elif command == PCommands.select_query:
                    query_string = message.args
                    user = message.user
                    print('Recieved query request from: {}'.format(user))
                    print('Query string: {}'.format(query_string))
                    token = message.token
                    if token in valid_tokens:
                        if user == valid_tokens[token]:
                            print('Processing query')
                            results = False
                            results_bool = False
                            # Try query
                            try: 
                                sql = message.args
                                db_connection = ordersDBConnect()
                                mycursor = db_connection.cursor()
                                mycursor.execute(sql)
                                results = mycursor.fetchall()
                            except Exception as e:
                                print(e)
                                results = False
                            if not (results is False):
                                results_bool = True
                            else:
                                results_bool = False
                            # Send client notification if query succeeded
                            results_bool_string = json.dumps(results_bool)
                            p.sendQueryResults(notified_socket, results_bool_string)
                            # If query succeeded send results object
                            if results_bool:
                                results_PObject = PObject(PObject.object_types.sql_results, results)
                                p.sendPObject(notified_socket, results_PObject)
                        else:
                            print('Error: User did not match token')
                            p.sendException(notified_socket, PExceptions.invalid_token)
                    else:
                        print('Error: Invalid token')
                        p.sendException(notified_socket, PExceptions.invalid_token)
                # Handle everything else
                else:
                    p.sendException(notified_socket, PExceptions.invalid_request)


    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]