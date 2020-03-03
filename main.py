import sys
from datetime import datetime
# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PySide2.QtCore import QFile, QDate
# pylint: enable=no-name-in-module

from LoginSystem import LoginInterface
from LoginForm import Ui_LoginForm
from MainMenu import Ui_MainMenu
from ui_windows import SalesOrderEntryForm, OpenSalesOrderDialog

from db_interface import (
    db_connect, query_allopen, translateResults, prettyHeaders
)

qt_app = QApplication(sys.argv)
login_sys = LoginInterface()

# Login Screen
class LoginForm(QWidget):
    def __init__(self):

        super(LoginForm, self).__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.ui.cancel.clicked.connect(self.cancel)
        self.ui.login.clicked.connect(self.login)
        self.action = 'none'
    
    def login(self):
        user = self.ui.username.text()
        password = self.ui.password.text()
        login_sys.login(user, password)
        if login_sys.authenticated:
            self.action = 'login'
            self.close()
        else:
            self.action = 'none'
            msg_box = QMessageBox()
            msg_box.setText('Login failed.')
            msg_box.setStyleSheet("QLabel{min-width: 75px;}")
            msg_box.exec_()


    def cancel(self):
        self.action = 'cancel'
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
        self.action = 'none'

    def logout(self):
        login_sys.logout()
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
        app = LoginForm()
        login_action = app.run()
        if login_action == 'login':
            app = MainMenu()
            main_action = app.run()
            if main_action == 'logout':
                Exit = False
            else:
                Exit = True
        else:
            Exit = True
