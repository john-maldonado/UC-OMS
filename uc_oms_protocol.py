import socket
import json
import pickle

class OMSUser():
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = ''
        self.authenticated = False

class PExceptions():
    invalid_token = 'INVAL_TOKEN'
    invalid_credentials = 'INVAL_CRED'
    invalid_request = 'INVAL_REQUEST'
    invalid_token_desc = 'Invalid token'
    invalid_credentials_desc = 'Invalid credentials'
    invalid_request_desc = 'Invalid request'
    exceptions_desc_dict = {
        invalid_token : invalid_token_desc,
        invalid_credentials : invalid_credentials_desc,
        invalid_request : invalid_request_desc
    }

class PCommands():
    connect = 'CONNECT'
    login = 'LOGIN'
    logout = 'LOGOUT'
    authenticate = 'AUTH'
    exception = 'EXCEPT'
    select_query = 'S_QUERY'
    insert_query = 'I_QUERY'
    update_query = 'U_QUERY'
    delete_query = 'D_QUERY'
    sendResults = 'RESULT'

class PMessage():
    def __init__(self, command: str = None, args: str = None, user: str = None, token: str = None):
        if not (command is None):
            self.command = command
        else:
            self.command = ''
        if not (args is None):
            self.args = args
        else:
            self.args = ''
        if not (user is None):
            self.user = user
        else:
            self.token = ''
        if not (command is None):
            self.token = token
        else:
            self.token = ''

    def getElements(self):
        elements = [self.command, self.args, self.user, self.token]
        return elements

    def toJSON(self):
        message_list = [self.command, self.args, self.user, self.token]
        message_json = json.dumps(message_list)
        return message_json

    def fromJSON(self, message_json: str):
        message_list = json.loads(message_json)
        self.command = message_list[0]
        self.args = message_list[1]
        self.user = message_list[2]
        self.token = message_list[3]
        return self

class PObject():
    class object_types():
        sql_results = 'SQL_RES'

    def __init__(self, object_type: str = None, an_object = None):
        self.object_type = object_type
        self.object = an_object

class Protocol(object):
    def __init__(self):
        self.main_header_length = 10

    def sendConnect(self, client_socket):
        command = PCommands.connect
        args = ''
        user = ''
        token = ''
        message = PMessage(command, args, user, token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendLogin(self, client_socket, user: OMSUser):
        command = PCommands.login
        args = user.password
        user = user.username
        token = ''
        message = PMessage(command, args, user, token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendLogout(self, client_socket, user: OMSUser):
        command = PCommands.logout
        args = ''
        message = PMessage(command, args, user.username, user.token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendAuthenticate(self, client_socket, token):
        command = PCommands.authenticate
        args = ''
        user = ''
        message = PMessage(command, args, user, token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendQuery(self, client_socket, query_type: str, user: OMSUser, query_string: str):
        command = query_type
        args = query_string
        message = PMessage(command, args, user.username, user.token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendPObject(self, client_socket, A_PObject: PObject):
        pickled_PObject = pickle.dumps(A_PObject)
        main_header = self.buildHeader(pickled_PObject, self.main_header_length)
        packet = main_header + pickled_PObject
        client_socket.send(packet)

    def receivePObject(self, client_socket):
        try:

            # Receive our "header" containing message length, it's size is defined and constant
            main_header = client_socket.recv(self.main_header_length)
            
            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(main_header):
                return False
            else:
                # Convert header to int value
                PObject_length = int(main_header.decode('utf-8').strip())

                # Recieve and return object
                pickled_PObject = self.receiveAllBytes(client_socket, PObject_length)
                the_PObject = pickle.loads(pickled_PObject)
                return the_PObject

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False

    def sendQueryResults(self, client_socket, results_json: str):
        command = PCommands.sendResults
        args = results_json
        user = ''
        token = ''
        message = PMessage(command, args, user, token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def sendException(self, client_socket, exception_code: str):
        command = PCommands.exception
        args = exception_code
        user = ''
        token = ''
        message = PMessage(command, args, user, token)
        packet = self.buildPacket(message)
        client_socket.send(packet)

    def buildPacket(self, message: PMessage):
        payload = message.toJSON().encode('utf-8')
        main_header = self.buildHeader(payload, self.main_header_length)
        packet = main_header + payload
        return packet        

    def buildHeader(self, data: bytes, header_length: int):
        header = f"{len(data):<{header_length}}".encode('utf-8')
        return header

    def receiveMessage(self, client_socket: socket.socket):

        try:

            # Receive our "header" containing message length, it's size is defined and constant
            main_header = client_socket.recv(self.main_header_length)
            
            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(main_header):
                return False
            else:
                # Convert header to int value
                message_length = int(main_header.decode('utf-8').strip())

                # Recieve and return message
                message_string = self.receiveAllBytes(client_socket, message_length)
                message = self.parseMessage(message_string)
                return message

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False

    def receiveAllBytes(self, client_socket: socket.socket, length: int):
        the_bytes = bytes()
        while True:
            remaining_length = length - len(the_bytes)
            chunk = client_socket.recv(remaining_length)
            the_bytes = the_bytes + chunk
            if len(the_bytes) == length:
                return the_bytes

    def parseMessage(self, message_json: str):
        message = PMessage().fromJSON(message_json)
        return message