# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SalesOrderEntryForm.ui'
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


class Ui_SalesOrderEntryForm(object):
    def setupUi(self, SalesOrderEntryForm):
        if SalesOrderEntryForm.objectName():
            SalesOrderEntryForm.setObjectName(u"SalesOrderEntryForm")
        SalesOrderEntryForm.resize(402, 184)
        SalesOrderEntryForm.setMinimumSize(QSize(402, 184))
        SalesOrderEntryForm.setMaximumSize(QSize(402, 184))
        self.label = QLabel(SalesOrderEntryForm)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 40, 71, 16))
        self.label_2 = QLabel(SalesOrderEntryForm)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 71, 16))
        self.label_3 = QLabel(SalesOrderEntryForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 102, 71, 16))
        self.label_4 = QLabel(SalesOrderEntryForm)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(210, 102, 71, 16))
        self.description = QLineEdit(SalesOrderEntryForm)
        self.description.setObjectName(u"description")
        self.description.setGeometry(QRect(90, 40, 291, 20))
        self.customer = QLineEdit(SalesOrderEntryForm)
        self.customer.setObjectName(u"customer")
        self.customer.setGeometry(QRect(90, 70, 291, 20))
        self.order_date = QDateEdit(SalesOrderEntryForm)
        self.order_date.setObjectName(u"order_date")
        self.order_date.setGeometry(QRect(90, 100, 110, 22))
        self.order_date.setCalendarPopup(True)
        self.due_date = QDateEdit(SalesOrderEntryForm)
        self.due_date.setObjectName(u"due_date")
        self.due_date.setGeometry(QRect(270, 100, 110, 22))
        self.due_date.setCalendarPopup(True)
        self.submit = QPushButton(SalesOrderEntryForm)
        self.submit.setObjectName(u"submit")
        self.submit.setGeometry(QRect(220, 150, 75, 23))
        self.cancel = QPushButton(SalesOrderEntryForm)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setGeometry(QRect(310, 150, 75, 23))
        self.label_5 = QLabel(SalesOrderEntryForm)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 10, 371, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.retranslateUi(SalesOrderEntryForm)

        self.submit.setDefault(True)


        QMetaObject.connectSlotsByName(SalesOrderEntryForm)
    # setupUi

    def retranslateUi(self, SalesOrderEntryForm):
        SalesOrderEntryForm.setWindowTitle(QCoreApplication.translate("SalesOrderEntryForm", u"Sales Order Entry", None))
        self.label.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Description:", None))
        self.label_2.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Customer:", None))
        self.label_3.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Order Date:", None))
        self.label_4.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Due Date:", None))
        self.submit.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Submit", None))
        self.cancel.setText(QCoreApplication.translate("SalesOrderEntryForm", u"Cancel", None))
        self.label_5.setText(QCoreApplication.translate("SalesOrderEntryForm", u"New Sales Order", None))
    # retranslateUi

