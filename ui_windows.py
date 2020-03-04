import operator

# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QInputDialog
from PySide2.QtCore import Qt, QFile, QDate, QAbstractTableModel, SIGNAL
# pylint: enable=no-name-in-module

from SalesOrderEntryForm import Ui_SalesOrderEntryForm
from SalesOrderEntryVerifyDialog import Ui_SalesOrderEntryVerifyDialog
from OpenSalesOrderDialog import Ui_OpenSalesOrderDialog
from TimeLogDialog import Ui_TimeLogDialog
from DateTimeEditDialog import Ui_DateTimeEditDialog

from db_interface import (
    db_connect, query_insertIntoSalesOrders, query_maxSalesOrder, query_timeLogBySO, translateResults, prettyHeaders, query_insertIntoTimeLog,
    query_deleteTimeLogByLogID, query_updateTimeLogClockOut, query_updateTimeLogSingleField, query_timeLogTotalTimeBySO
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
        self.ui.clockIn.clicked.connect(self.clockIn)
        self.ui.clockOut.clicked.connect(self.clockOut)
        self.ui.close.clicked.connect(self.exit)
        self.ui.deleteButton.clicked.connect(self.delete)
        self.ui.edit.clicked.connect(self.edit)
        self.ui.total.clicked.connect(self.total)
        self.soSearch()
    
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
        db_connection = db_connect()
        results, fields = query_timeLogBySO(db_connection, self.sales_order)
        data = translateResults(results, fields)
        headers = prettyHeaders(fields)
        self.populateTable(data, headers)
        self.table_data = data
        self.table_headers = headers

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