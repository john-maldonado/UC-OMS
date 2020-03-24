import sys
from datetime import datetime
# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PySide2.QtCore import QFile, QDate
# pylint: enable=no-name-in-module

from LoginForm import Ui_LoginForm
from MainMenu import Ui_MainMenu
from uc_oms_ui import LoginForm, MainMenu, SalesOrderEntryForm, OpenSalesOrderDialog, TimeLogDialog, SOSearchDialog

from uc_oms_db_queries import (
    prettyHeaders, translateResults, query_selectAllOpen
)

from uc_oms_protocol import Protocol, PCommands

import socket

class OMSUser():
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.token = ''
        self.authenticated = False

# Define Qt App
qt_app = QApplication(sys.argv)
# Define Protocal Instance
p = Protocol()
# Define User Instance
u = OMSUser()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
IP = "10.0.0.119"
PORT = 4444

# Create Socket
s.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
s.setblocking(False)

if __name__ == "__main__":
    Exit = False
    while (not Exit):

        # Initiate Connection
        p.sendConnect(s)
        s.setblocking(True)
        message = p.receiveMessage(s)
        s.setblocking(False)
        if message is False:
            print('Failed to connect to server')
            input('Press Enter to continue')
        else:
            command = message.command
            if command == PCommands.connect:
                print('Connected to server!')
                # Show Login Screen
                app = LoginForm(qt_app, s, u)
                login_action = app.run()
                if login_action == 'login':
                    # Proceed to Main Menu
                    app = MainMenu(qt_app, s, u)
                    main_action = app.run()
                    if main_action == 'logout':
                        Exit = False
                    else:
                        Exit = True
                else:
                    Exit = True
