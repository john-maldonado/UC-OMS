# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SOSearchDialog.ui'
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


class Ui_SOSearchDialog(object):
    def setupUi(self, SOSearchDialog):
        if SOSearchDialog.objectName():
            SOSearchDialog.setObjectName(u"SOSearchDialog")
        SOSearchDialog.resize(570, 450)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SOSearchDialog.sizePolicy().hasHeightForWidth())
        SOSearchDialog.setSizePolicy(sizePolicy)
        self.label = QLabel(SOSearchDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(6, 10, 561, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.field1 = QComboBox(SOSearchDialog)
        self.field1.setObjectName(u"field1")
        self.field1.setGeometry(QRect(20, 50, 121, 21))
        self.field1.setFocusPolicy(Qt.NoFocus)
        self.textInput1 = QLineEdit(SOSearchDialog)
        self.textInput1.setObjectName(u"textInput1")
        self.textInput1.setGeometry(QRect(160, 50, 241, 21))
        self.textInput1.setFocusPolicy(Qt.NoFocus)
        self.joinOperator = QComboBox(SOSearchDialog)
        self.joinOperator.setObjectName(u"joinOperator")
        self.joinOperator.setGeometry(QRect(20, 80, 121, 21))
        self.joinOperator.setFocusPolicy(Qt.NoFocus)
        self.field2 = QComboBox(SOSearchDialog)
        self.field2.setObjectName(u"field2")
        self.field2.setGeometry(QRect(20, 110, 121, 21))
        self.field2.setFocusPolicy(Qt.NoFocus)
        self.textInput2 = QLineEdit(SOSearchDialog)
        self.textInput2.setObjectName(u"textInput2")
        self.textInput2.setGeometry(QRect(160, 110, 241, 21))
        self.textInput2.setFocusPolicy(Qt.NoFocus)
        self.openSalesOrder = QPushButton(SOSearchDialog)
        self.openSalesOrder.setObjectName(u"openSalesOrder")
        self.openSalesOrder.setGeometry(QRect(20, 410, 141, 23))
        self.close = QPushButton(SOSearchDialog)
        self.close.setObjectName(u"close")
        self.close.setGeometry(QRect(477, 410, 75, 23))
        self.dateInput1 = QDateEdit(SOSearchDialog)
        self.dateInput1.setObjectName(u"dateInput1")
        self.dateInput1.setGeometry(QRect(160, 50, 241, 21))
        self.dateInput1.setFocusPolicy(Qt.NoFocus)
        self.dateInput1.setCalendarPopup(True)
        self.dateInput2 = QDateEdit(SOSearchDialog)
        self.dateInput2.setObjectName(u"dateInput2")
        self.dateInput2.setGeometry(QRect(160, 110, 241, 21))
        self.dateInput2.setFocusPolicy(Qt.NoFocus)
        self.dateInput2.setCalendarPopup(True)
        self.tableView = QTableView(SOSearchDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(20, 150, 531, 241))
        self.searchButton = QPushButton(SOSearchDialog)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setGeometry(QRect(440, 49, 81, 23))
        self.searchButton.setFocusPolicy(Qt.NoFocus)
        self.dateInput2.raise_()
        self.dateInput1.raise_()
        self.label.raise_()
        self.field1.raise_()
        self.textInput1.raise_()
        self.joinOperator.raise_()
        self.field2.raise_()
        self.textInput2.raise_()
        self.openSalesOrder.raise_()
        self.close.raise_()
        self.tableView.raise_()
        self.searchButton.raise_()

        self.retranslateUi(SOSearchDialog)

        QMetaObject.connectSlotsByName(SOSearchDialog)
    # setupUi

    def retranslateUi(self, SOSearchDialog):
        SOSearchDialog.setWindowTitle(QCoreApplication.translate("SOSearchDialog", u"SO Search", None))
        self.label.setText(QCoreApplication.translate("SOSearchDialog", u"Sales Order Search", None))
        self.openSalesOrder.setText(QCoreApplication.translate("SOSearchDialog", u"Open Sales Order Detail", None))
        self.close.setText(QCoreApplication.translate("SOSearchDialog", u"Close", None))
        self.searchButton.setText(QCoreApplication.translate("SOSearchDialog", u"Search", None))
    # retranslateUi

