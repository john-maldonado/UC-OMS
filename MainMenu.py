# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainMenu.ui'
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


class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        if MainMenu.objectName():
            MainMenu.setObjectName(u"MainMenu")
        MainMenu.resize(750, 350)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainMenu.sizePolicy().hasHeightForWidth())
        MainMenu.setSizePolicy(sizePolicy)
        self.label = QLabel(MainMenu)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(240, 20, 271, 91))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.viewOpenOrders = QPushButton(MainMenu)
        self.viewOpenOrders.setObjectName(u"viewOpenOrders")
        self.viewOpenOrders.setGeometry(QRect(100, 130, 151, 51))
        self.viewOpenOrders.setAutoDefault(True)
        self.newSalesOrder = QPushButton(MainMenu)
        self.newSalesOrder.setObjectName(u"newSalesOrder")
        self.newSalesOrder.setGeometry(QRect(300, 130, 151, 51))
        self.newSalesOrder.setAutoDefault(True)
        self.salesOrderSearch = QPushButton(MainMenu)
        self.salesOrderSearch.setObjectName(u"salesOrderSearch")
        self.salesOrderSearch.setGeometry(QRect(100, 220, 151, 51))
        self.salesOrderSearch.setAutoDefault(True)
        self.updateSalesOrder = QPushButton(MainMenu)
        self.updateSalesOrder.setObjectName(u"updateSalesOrder")
        self.updateSalesOrder.setGeometry(QRect(500, 130, 151, 51))
        self.updateSalesOrder.setAutoDefault(True)
        self.timeLog = QPushButton(MainMenu)
        self.timeLog.setObjectName(u"timeLog")
        self.timeLog.setGeometry(QRect(300, 220, 151, 51))
        self.timeLog.setAutoDefault(True)
        self.logout = QPushButton(MainMenu)
        self.logout.setObjectName(u"logout")
        self.logout.setGeometry(QRect(500, 220, 151, 51))
        self.logout.setAutoDefault(True)
        QWidget.setTabOrder(self.viewOpenOrders, self.newSalesOrder)
        QWidget.setTabOrder(self.newSalesOrder, self.updateSalesOrder)
        QWidget.setTabOrder(self.updateSalesOrder, self.salesOrderSearch)
        QWidget.setTabOrder(self.salesOrderSearch, self.timeLog)
        QWidget.setTabOrder(self.timeLog, self.logout)

        self.retranslateUi(MainMenu)

        QMetaObject.connectSlotsByName(MainMenu)
    # setupUi

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QCoreApplication.translate("MainMenu", u"UC Order Management System", None))
        self.label.setText(QCoreApplication.translate("MainMenu", u"Ultimate Controls, LLC. \n"
" Order Management System", None))
        self.viewOpenOrders.setText(QCoreApplication.translate("MainMenu", u"View Open Orders", None))
        self.newSalesOrder.setText(QCoreApplication.translate("MainMenu", u"New Sales Order", None))
        self.salesOrderSearch.setText(QCoreApplication.translate("MainMenu", u"Sales Order Search", None))
        self.updateSalesOrder.setText(QCoreApplication.translate("MainMenu", u"Update Sales Order", None))
        self.timeLog.setText(QCoreApplication.translate("MainMenu", u"Time Log", None))
        self.logout.setText(QCoreApplication.translate("MainMenu", u"Logout", None))
    # retranslateUi

