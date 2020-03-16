import sys
from datetime import datetime
# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PySide2.QtCore import QFile, QDate
# pylint: enable=no-name-in-module

from LoginForm import Ui_LoginForm
from MainMenu import Ui_MainMenu
from ui_windows import SalesOrderEntryForm, OpenSalesOrderDialog, TimeLogDialog, SOSearchDialog

from db_interface import (
    db_connect, query_allopen, translateResults, prettyHeaders
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

# Login Screen
class LoginForm(QWidget):
    def __init__(self):

        super(LoginForm, self).__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.login.clicked.connect(self.login)
        self.ui.password.returnPressed.connect(self.login)
        self.action = 'none'
        self.ui.username.setFocus()
    
    def login(self):
        u.username = self.ui.username.text()
        u.password = self.ui.password.text()
        p.sendLogin(s, u.username, u.password)
        s.setblocking(True)
        message = p.receiveMessage(s)
        s.setblocking(False)
        if message.command == PCommands.authenticate:
            token = message.token
            print('Succesfully Authenticated!')
            print('Token: {}'.format(token))
            u.authenticated = True
            u.token = token
        if u.authenticated:
            self.action = 'login'
            self.close()
        else:
            self.action = 'none'
            msg_box = QMessageBox()
            msg_box.setText('Login failed.')
            msg_box.setStyleSheet("QLabel{min-width: 75px;}")
            msg_box.exec_()


    def exit(self):
        self.action = 'exit'
        self.close()


    def run(self):
        self.show()
        qt_app.exec_()
        return self.action

# Main Menu
class MainMenu(QWidget):
    def __init__(self):

        super(MainMenu, self).__init__()
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
        self.ui.newSalesOrder.clicked.connect(self.newSalesOrder)
        self.ui.logout.clicked.connect(self.logout)
        self.ui.viewOpenOrders.clicked.connect(self.reviewOpenSalesOrders)
        self.ui.timeLog.clicked.connect(self.timeLog)
        self.ui.salesOrderSearch.clicked.connect(self.soSearch)
        self.action = 'none'

    def timeLog(self):
        dialog = TimeLogDialog()
        dialog.exec_()

    def soSearch(self):
        dialog = SOSearchDialog()
        dialog.exec_()

    def logout(self):
        print('Requesting logout')
        p.sendLogout(s, u.username, u.token)
        s.setblocking(True)
        message = p.receiveMessage(s)
        s.setblocking(False)
        if message.command == PCommands.logout:
            u.token = ''
            u.authenticated = False
            print('Logged Out')
        self.action = 'logout'
        self.close()
    
    def newSalesOrder(self):
        print('New Sales Order')
        newSalesOrderWindow = SalesOrderEntryForm()
        newSalesOrderWindow.exec_()
    
    def reviewOpenSalesOrders(self):
        print('Review Open Sales Orders')
        dialog = OpenSalesOrderDialog()
        db_connection = db_connect()
        results, fields = query_allopen(db_connection)
        data = translateResults(results, fields)
        headers = prettyHeaders(fields)
        dialog.populateTable(data, headers)
        dialog.exec_()

    def run(self):
        self.show()
        qt_app.exec_()
        return self.action

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
                app = LoginForm()
                login_action = app.run()
                if login_action == 'login':
                    # Proceed to Main Menu
                    app = MainMenu()
                    main_action = app.run()
                    if main_action == 'logout':
                        Exit = False
                    else:
                        Exit = True
                else:
                    Exit = True
