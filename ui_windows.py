import operator

# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog
from PySide2.QtCore import Qt, QFile, QDate, QAbstractTableModel, SIGNAL
# pylint: enable=no-name-in-module

from SalesOrderEntryForm import Ui_SalesOrderEntryForm
from SalesOrderEntryVerifyDialog import Ui_SalesOrderEntryVerifyDialog
from OpenSalesOrderDialog import Ui_OpenSalesOrderDialog
from TimeLogDialog import Ui_TimeLogDialog

from db_interface import (
    db_connect, query_insertIntoSalesOrders, query_maxSalesOrder, query_timeLogBySO, translateResults, prettyHeaders
)

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
            db_connection = db_connect()
            maxSalesOrder = query_maxSalesOrder(db_connection)
            maxSalesOrder = maxSalesOrder[2 : : ]
            maxSalesOrderInt = int(maxSalesOrder)
            newSalesOrderInt = maxSalesOrderInt + 1
            newSalesOrder = "SO{}".format(newSalesOrderInt)
            salesOrder = newSalesOrder
            query_insertIntoSalesOrders(db_connection, salesOrder, description, customer, order_date, due_date)
            msgbox = QMessageBox()
            msgbox.setText("Order entered successfully.<br>SO Number: {}".format(salesOrder))
            msgbox.setStyleSheet("QLabel{min-width: 175px;}")
            msgbox.setWindowTitle('Sales Order Entry')
            msgbox.exec_()
            self.close()

    def cancel(self):
        print('Cancel')
        self.close()

# Open Sales Orders Dialog
class OpenSalesOrderDialog(QDialog):
    def __init__(self):
        super(OpenSalesOrderDialog, self).__init__()
        self.ui = Ui_OpenSalesOrderDialog()
        self.ui.setupUi(self)

    def populateTable(self, data_list, header):
        table_model = MyTableModel(self, data_list, header)
        self.ui.tableView.setModel(table_model)
         # set column width to fit contents (set font first!)
        self.ui.tableView.resizeColumnsToContents()
        # enable sorting
        self.ui.tableView.setSortingEnabled(True)
        
# Time Log Dialog
class TimeLogDialog(QDialog):
    def __init__(self):
        super(TimeLogDialog, self).__init__()
        self.ui = Ui_TimeLogDialog()
        self.ui.setupUi(self)
        self.ui.soSearch.clicked.connect(self.soSearch)
        
    def soSearch(self):
        # input_box = QInputDialog()
        # input_box.setLabelText('Sales Order Number:')
        # response = input_box.exec_()
        text, okPressed = QInputDialog.getText(self, "SO Search", "SO Number:")
        if okPressed:
            salesOrder = text
            db_connection = db_connect()
            results, fields = query_timeLogBySO(db_connection, salesOrder)
            data = translateResults(results, fields)
            headers = prettyHeaders(fields)
            self.populateTable(data, headers)


    def populateTable(self, data_list, header):
        table_model = MyTableModel(self, data_list, header)
        self.ui.tableView.setModel(table_model)
         # set column width to fit contents (set font first!)
        self.ui.tableView.resizeColumnsToContents()
        # enable sorting
        self.ui.tableView.setSortingEnabled(True)

# Table Model Definition
class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
                             key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))