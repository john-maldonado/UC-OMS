# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PySide2.QtCore import QFile, QDate
# pylint: enable=no-name-in-module

from SalesOrderEntryForm import Ui_SalesOrderEntryForm
from SalesOrderEntryVerifyDialog import Ui_SalesOrderEntryVerifyDialog

# Sales Order Entry Verification Dialog
class SalesOrderEntryVerifyDialog(QDialog):
    def __init__(self):

        super(SalesOrderEntryVerifyDialog, self).__init__()
        self.ui = Ui_SalesOrderEntryVerifyDialog()
        self.ui.setupUi(self)

# Sales Order Entry Form
class SalesOrderEntryForm(QDialog):
    def __init__(self):

        super(SalesOrderEntryForm, self).__init__()
        self.ui = Ui_SalesOrderEntryForm()
        self.ui.setupUi(self)
        self.ui.order_date.setDate(QDate.currentDate())
        self.ui.due_date.setDate(QDate.currentDate())
        self.ui.submit.clicked.connect(self.submit)
        self.ui.cancel.clicked.connect(self.cancel)


    def submit(self):
        description = self.ui.description.text()
        customer = self.ui.customer.text()
        order_date = self.ui.order_date.date().toPython()
        due_date = self.ui.due_date.date().toPython()
        order_details = "<p align='left'>Description: {} <br>Customer: {}<br>Order Date: {}<br>Due Date: {}</p>".format(description, customer, order_date, due_date)
        dialog = SalesOrderEntryVerifyDialog()
        dialog.setWindowTitle('Sales Order Entry')
        dialog.ui.textBrowser.setText(order_details)
        response = dialog.exec_()
        if response == 1:
            print('Yes')
            print('SQL INSERT')
            msgbox = QMessageBox()
            msgbox.setText('Order entered successfully.')
            msgbox.setStyleSheet("QLabel{min-width: 175px;}")
            msgbox.setWindowTitle('Sales Order Entry')
            msgbox.exec_()
            self.close()
        elif response == 0:
            print('No')

    def cancel(self):
        print('Cancel')
        self.close()