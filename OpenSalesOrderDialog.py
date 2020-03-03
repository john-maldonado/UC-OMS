# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OpenSalesOrderDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_OpenSalesOrderDialog(object):
    def setupUi(self, OpenSalesOrderDialog):
        if OpenSalesOrderDialog.objectName():
            OpenSalesOrderDialog.setObjectName(u"OpenSalesOrderDialog")
        OpenSalesOrderDialog.resize(740, 470)
        self.buttonBox = QDialogButtonBox(OpenSalesOrderDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 430, 701, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.tableView = QTableView(OpenSalesOrderDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(20, 50, 701, 361))
        self.label = QLabel(OpenSalesOrderDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 741, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.retranslateUi(OpenSalesOrderDialog)
        self.buttonBox.accepted.connect(OpenSalesOrderDialog.accept)
        self.buttonBox.rejected.connect(OpenSalesOrderDialog.reject)

        QMetaObject.connectSlotsByName(OpenSalesOrderDialog)
    # setupUi

    def retranslateUi(self, OpenSalesOrderDialog):
        OpenSalesOrderDialog.setWindowTitle(QCoreApplication.translate("OpenSalesOrderDialog", u"Open Sales Orders", None))
        self.label.setText(QCoreApplication.translate("OpenSalesOrderDialog", u"Open Sales Orders", None))
    # retranslateUi

