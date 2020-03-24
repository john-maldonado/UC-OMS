import operator
import socket

# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog, QComboBox
from PySide2.QtCore import Qt, QFile, QDate, QAbstractTableModel, SIGNAL
# pylint: enable=no-name-in-module

from LoginForm import Ui_LoginForm
from MainMenu import Ui_MainMenu
from SalesOrderEntryForm import Ui_SalesOrderEntryForm
from SalesOrderEntryVerifyDialog import Ui_SalesOrderEntryVerifyDialog
from OpenSalesOrderDialog import Ui_OpenSalesOrderDialog
from TimeLogDialog import Ui_TimeLogDialog
from DateTimeEditDialog import Ui_DateTimeEditDialog
from SOSearchDialog import Ui_SOSearchDialog

from uc_oms_protocol import (
    Protocol, OMSUser, PCommands
)

from db_interface import (
    db_connect, query_insertIntoTimeLog,
    query_deleteTimeLogByLogID, query_updateTimeLogClockOut, query_updateTimeLogSingleField, query_timeLogTotalTimeBySO
)

from uc_oms_db_queries import (
    prettyHeaders, translateResults, query_selectAllOpen, query_insertIntoSalesOrders, query_selectMaxSalesOrder, query_selectTimeLogBySO
)

# Login Screen
class LoginForm(QWidget):
    def __init__(self, app: QApplication, s: socket.socket, u: OMSUser):

        super(LoginForm, self).__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.ui.exit.clicked.connect(self.exit)
        self.ui.login.clicked.connect(self.login)
        self.ui.password.returnPressed.connect(self.login)
        self.action = 'none'
        self.ui.username.setFocus()
        self.app = app
        self.s = s
        self.u = u

    
    def login(self):
        self.u.username = self.ui.username.text()
        self.u.password = self.ui.password.text()
        Protocol().sendLogin(self.s, self.u)
        self.s.setblocking(True)
        message = Protocol().receiveMessage(self.s)
        self.s.setblocking(False)
        if message.command == PCommands.authenticate:
            token = message.token
            print('Succesfully Authenticated!')
            print('Token: {}'.format(token))
            self.u.authenticated = True
            self.u.token = token
        if self.u.authenticated:
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
        self.app.exec_()
        return self.action

# Main Menu
class MainMenu(QWidget):
    def __init__(self, app: QApplication, s: socket.socket, u: OMSUser):

        super(MainMenu, self).__init__()
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
        self.ui.newSalesOrder.clicked.connect(self.newSalesOrder)
        self.ui.logout.clicked.connect(self.logout)
        self.ui.viewOpenOrders.clicked.connect(self.reviewOpenSalesOrders)
        self.ui.timeLog.clicked.connect(self.timeLog)
        self.ui.salesOrderSearch.clicked.connect(self.soSearch)
        self.action = 'none'
        self.app = app
        self.s = s
        self.u = u


    def timeLog(self):
        dialog = TimeLogDialog(self.s, self.u)
        dialog.exec_()

    def soSearch(self):
        dialog = SOSearchDialog()
        dialog.exec_()

    def logout(self):
        print('Requesting logout')
        Protocol().sendLogout(self.s, self.u)
        self.s.setblocking(True)
        message = Protocol().receiveMessage(self.s)
        self.s.setblocking(False)
        if message.command == PCommands.logout:
            self.u.token = ''
            self.u.authenticated = False
            print('Logged Out')
        self.action = 'logout'
        self.close()
    
    def newSalesOrder(self):
        print('New Sales Order')
        newSalesOrderWindow = SalesOrderEntryForm(self.s, self.u)
        newSalesOrderWindow.exec_()
    
    def reviewOpenSalesOrders(self):
        print('Review Open Sales Orders')
        dialog = OpenSalesOrderDialog()
        results, fields, exception = query_selectAllOpen(self.s, self.u)
        if exception is False:
            data = translateResults(results, fields)
            headers = prettyHeaders(fields)
            dialog.populateTable(data, headers)
            dialog.exec_()
        else:
            QMessageBox.warning(self, 'Error', 'Query Exception: {}'.format(exception), QMessageBox.Ok)

    def run(self):
        self.show()
        self.app.exec_()
        return self.action

# Sales Order Entry Verification Dialog
class SalesOrderEntryVerifyDialog(QDialog):
    def __init__(self):

        super(SalesOrderEntryVerifyDialog, self).__init__()
        self.ui = Ui_SalesOrderEntryVerifyDialog()
        self.ui.setupUi(self)

# Sales Order Entry Form
class SalesOrderEntryForm(QDialog):
    def __init__(self, s : socket.socket, u : OMSUser):

        super(SalesOrderEntryForm, self).__init__()
        self.ui = Ui_SalesOrderEntryForm()
        self.ui.setupUi(self)
        self.ui.order_date.setDate(QDate.currentDate())
        self.ui.due_date.setDate(QDate.currentDate())
        self.ui.submit.clicked.connect(self.submit)
        self.ui.cancel.clicked.connect(self.cancel)
        self.s = s
        self.u = u

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
            results, _, exception = query_selectMaxSalesOrder(self.s, self.u)
            if exception is False:
                result = results[0][0]
                maxSalesOrder = result[2 : : ]
                maxSalesOrderInt = int(maxSalesOrder)
                newSalesOrderInt = maxSalesOrderInt + 1
                newSalesOrder = "SO{}".format(newSalesOrderInt)
                salesOrder = newSalesOrder
                result, exception = query_insertIntoSalesOrders(self.s, self.u, salesOrder, description, customer, order_date, due_date)
                if exception is False:
                    if result:
                        msgbox = QMessageBox()
                        msgbox.setText("Order entered successfully.<br>SO Number: {}".format(salesOrder))
                        msgbox.setStyleSheet("QLabel{min-width: 175px;}")
                        msgbox.setWindowTitle('Sales Order Entry')
                        msgbox.exec_()
                        self.close()
                    else:
                        QMessageBox.warning(self, 'Error', 'Error: Insert Query Failed', QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, 'Error', 'Query Exception: {}'.format(exception), QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Error', 'Query Exception: {}'.format(exception), QMessageBox.Ok)

    def cancel(self):
        self.close()

# SO Search Dialog
class SOSearchDialog(QDialog):
    def __init__(self):
        super(SOSearchDialog, self).__init__()
        self.ui = Ui_SOSearchDialog()
        self.ui.setupUi(self)
        self.ui.dateInput1.setVisible(False)
        self.ui.dateInput2.setVisible(False)
        self.ui.dateInput1.setDate(QDate.currentDate())
        self.ui.dateInput2.setDate(QDate.currentDate())
        self.search_fields = ['so_number', 'customer', 'so_id', 'order_date', 'due_date']
        headers = prettyHeaders(self.search_fields)
        self.ui.field1.addItems(headers)
        self.ui.field2.addItems(headers)
        self.join_operators = ['NONE', 'AND', 'OR', 'TO']
        self.ui.joinOperator.addItems(self.join_operators)
        self.ui.field2.setDisabled(True)
        self.ui.textInput2.setDisabled(True)
        self.ui.close.clicked.connect(self.close)
        self.ui.joinOperator.activated.connect(self.disable2ndField)
        self.ui.field1.activated.connect(self.controlField1Visibility)
        self.ui.field2.activated.connect(self.controlField2Visibility)

    def controlField1Visibility(self):
        index = self.ui.field1.currentIndex()
        field = self.search_fields[index]
        print(field)
        if (field == 'order_date') or (field == 'due_date'):
            self.ui.textInput1.setVisible(False)
            self.ui.dateInput1.setVisible(True)
            print('ping')
        else:
            self.ui.textInput1.setVisible(True)
            self.ui.dateInput1.setVisible(False)
            print('pong')

    def controlField2Visibility(self):
        index = self.ui.field2.currentIndex()
        field = self.search_fields[index]
        if (field == 'order_date') or (field == 'due_date'):
            self.ui.textInput2.setVisible(False)
            self.ui.dateInput2.setVisible(True)
            print('ping')
        else:
            self.ui.textInput2.setVisible(True)
            self.ui.dateInput2.setVisible(False)
            print('pong')

    def disable2ndField(self):
        index = self.ui.joinOperator.currentIndex()
        if index == 0:
            self.ui.textInput2.setDisabled(True)
            self.ui.field2.setDisabled(True)
            self.ui.dateInput2.setDisabled(True)
        else:
            self.ui.textInput2.setDisabled(False)
            self.ui.field2.setDisabled(False)
            self.ui.dateInput2.setDisabled(False)

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
    def __init__(self, s: socket.socket, u: OMSUser):
        super(TimeLogDialog, self).__init__()
        self.ui = Ui_TimeLogDialog()
        self.ui.setupUi(self)
        self.ui.soSearch.clicked.connect(self.soSearch)
        self.ui.clockIn.clicked.connect(self.clockIn)
        self.ui.clockOut.clicked.connect(self.clockOut)
        self.ui.close.clicked.connect(self.exit)
        self.ui.deleteButton.clicked.connect(self.delete)
        self.ui.edit.clicked.connect(self.edit)
        self.ui.total.clicked.connect(self.total)
        self.soSearch()
        self.s = s
        self.u = u
    
    def clockIn(self):
        sales_order = self.sales_order
        db_connection = db_connect()
        query_insertIntoTimeLog(db_connection, sales_order)
        self.refreshTable()
    
    def clockOut(self):
        log_id = self.getSelectedTableDataByColumn(0)
        clockin_ts = self.getSelectedTableDataByColumn(2)
        clockout_ts = self.getSelectedTableDataByColumn(3)
        if not (log_id == None):
            if not (clockin_ts == None):
                if clockout_ts == None:
                    text, okPressed = QInputDialog.getText(self, "Activity", "Activity:")
                    if okPressed:
                        activity = text
                        db_connection = db_connect()
                        query_updateTimeLogClockOut(db_connection, log_id, activity)
                        self.refreshTable()
                else:
                    QMessageBox.warning(self, 'Error', 'Error: Already clocked out', QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Error', 'Error: Not clocked in', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Error', 'Error: No time log entry selected', QMessageBox.Ok)

    def total(self):
        db_connection = db_connect()
        total_time = query_timeLogTotalTimeBySO(db_connection, self.sales_order)
        msg_box_text = "Sales Order: {}<br>Total Time: {} hrs".format(self.sales_order, total_time)
        QMessageBox.information(self, 'Total Time', msg_box_text, QMessageBox.Ok)

    def delete(self):
        log_id = self.getSelectedTableDataByColumn(0)
        so_number = self.getSelectedTableDataByColumn(1)
        activity = self.getSelectedTableDataByColumn(4)
        if not (log_id == None):
            message = 'Are you sure you want to delete this entry?<br>Log ID: {}<br>Sales Order: {}<br>Activity: {}'.format(log_id, so_number, activity)
            reply = QMessageBox.question(self, 'Delete', message, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                db_connection = db_connect()
                query_deleteTimeLogByLogID(db_connection, log_id)
                self.refreshTable()
        else:
            QMessageBox.warning(self, 'Error', 'Error: No time log entry selected', QMessageBox.Ok)

    def edit(self):
        # row_index = self.ui.tableView.selectionModel().currentIndex().row()
        column_index = self.ui.tableView.selectionModel().currentIndex().column()
        log_id = self.getSelectedTableDataByColumn(0)
        # index = self.ui.tableView.model().index(row_index, column_index)
        # item_data = self.ui.tableView.model().itemData(index)
        # data = item_data.get(0)
        header = self.table_headers[column_index]
        if not (log_id == None):
            if header == "Log ID":
                QMessageBox.warning(self, 'Error', 'Error: Can not edit Log ID', QMessageBox.Ok)
            elif header == "SO Number":
                text, okPressed = QInputDialog.getText(self, "Edit SO Number", "SO Number:")
                if okPressed:
                    so_number = text
                    field = 'so_number'
                    db_connection = db_connect()
                    query_updateTimeLogSingleField(db_connection, log_id, field, so_number)
                    self.refreshTable()
            elif header == "Clock In":
                dialog = DateTimeEditDialog('Edit Clock In', 'Clock In Time:')
                dateTime, okPressed = dialog.getDateTime()
                if okPressed:
                    clockin_ts = dateTime.toPython()
                    field = 'clockin_ts'
                    query_updateTimeLogSingleField(db_connection, log_id, field, clockin_ts)
                    self.refreshTable()
            elif header == "Clock Out":
                dialog = DateTimeEditDialog('Edit Clock Out', 'Clock Out Time:')
                dateTime, okPressed = dialog.getDateTime()
                if okPressed:
                    clockout_ts = dateTime.toPython()
                    field = 'clockout_ts'
                    db_connection = db_connect()
                    query_updateTimeLogSingleField(db_connection, log_id, field, clockout_ts)
                    self.refreshTable()
            elif header == "Activity":
                text, okPressed = QInputDialog.getText(self, "Edit Activity", "Activity:")
                if okPressed:
                    activity = text
                    field = 'activity'
                    db_connection = db_connect()
                    query_updateTimeLogSingleField(db_connection, log_id, field, activity)
                    self.refreshTable()
        else:
            QMessageBox.warning(self, 'Error', 'Error: No time log entry selected', QMessageBox.Ok)

    def exit(self):
        self.close()
        
    def soSearch(self):
        text, okPressed = QInputDialog.getText(self, "SO Search", "SO Number:")
        if okPressed:
            self.sales_order = text
            self.refreshTable()
    
    def refreshTable(self):
        results, fields, exception = query_selectTimeLogBySO(self.s, self.u, self.sales_order)
        if exception is False:
            data = translateResults(results, fields)
            headers = prettyHeaders(fields)
            self.populateTable(data, headers)
            self.table_data = data
            self.table_headers = headers
        else:
            QMessageBox.warning(self, 'Error', 'Query Exception: {}'.format(exception), QMessageBox.Ok)

    def populateTable(self, data_list, header):
        table_model = MyTableModel(self, data_list, header)
        self.ui.tableView.setModel(table_model)
         # set column width to fit contents (set font first!)
        self.ui.tableView.resizeColumnsToContents()
        # enable sorting
        self.ui.tableView.setSortingEnabled(True)

    def getSelectedTableDataByColumn(self, column_index):
        row_index = self.ui.tableView.selectionModel().currentIndex().row()
        index = self.ui.tableView.model().index(row_index, column_index)
        item_data = self.ui.tableView.model().itemData(index)
        return item_data.get(0)

class DateTimeEditDialog(QDialog):
    def __init__(self, windowTitle, labelText):
        super(DateTimeEditDialog, self).__init__()
        self.ui = Ui_DateTimeEditDialog()
        self.ui.setupUi(self)
        self.ui.dateTimeEdit.setDate(QDate.currentDate())
        self.setWindowTitle(windowTitle)
        self.ui.label.setText(labelText)

    def getDateTime(self):
        response = self.exec_()
        return self.ui.dateTimeEdit.dateTime(), response

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