import sys
# pylint: disable=no-name-in-module
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from PySide2.QtCore import QFile, QDate
# pylint: enable=no-name-in-module

from MainMenu import Ui_MainMenu
from ui_windows import SalesOrderEntryForm

qt_app = QApplication(sys.argv)

# Main Menu
class MainMenu(QWidget):
    def __init__(self):

        super(MainMenu, self).__init__()
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
        self.ui.newSalesOrder.clicked.connect(self.newSalesOrder)
    
    def newSalesOrder(self):
        print('New Sales Order')
        newSalesOrderWindow = SalesOrderEntryForm()
        newSalesOrderWindow.exec_()

    def run(self):
        self.show()
        qt_app.exec_()

if __name__ == "__main__":
    app = MainMenu()
    app.run()