# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeLogDialog.ui'
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


class Ui_TimeLogDialog(object):
    def setupUi(self, TimeLogDialog):
        if TimeLogDialog.objectName():
            TimeLogDialog.setObjectName(u"TimeLogDialog")
        TimeLogDialog.resize(582, 391)
        self.tableView = QTableView(TimeLogDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(10, 50, 461, 321))
        self.label = QLabel(TimeLogDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 561, 20))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.soSearch = QPushButton(TimeLogDialog)
        self.soSearch.setObjectName(u"soSearch")
        self.soSearch.setGeometry(QRect(490, 50, 80, 23))
        self.clockIn = QPushButton(TimeLogDialog)
        self.clockIn.setObjectName(u"clockIn")
        self.clockIn.setGeometry(QRect(490, 80, 80, 23))
        self.clockOut = QPushButton(TimeLogDialog)
        self.clockOut.setObjectName(u"clockOut")
        self.clockOut.setGeometry(QRect(490, 110, 80, 23))
        self.edit = QPushButton(TimeLogDialog)
        self.edit.setObjectName(u"edit")
        self.edit.setGeometry(QRect(490, 140, 80, 23))
        self.deleteButton = QPushButton(TimeLogDialog)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setGeometry(QRect(490, 170, 80, 23))
        self.close = QPushButton(TimeLogDialog)
        self.close.setObjectName(u"close")
        self.close.setGeometry(QRect(490, 350, 80, 23))

        self.retranslateUi(TimeLogDialog)

        QMetaObject.connectSlotsByName(TimeLogDialog)
    # setupUi

    def retranslateUi(self, TimeLogDialog):
        TimeLogDialog.setWindowTitle(QCoreApplication.translate("TimeLogDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("TimeLogDialog", u"Sales Order Time Log", None))
        self.soSearch.setText(QCoreApplication.translate("TimeLogDialog", u"SO Search", None))
        self.clockIn.setText(QCoreApplication.translate("TimeLogDialog", u"Clock In", None))
        self.clockOut.setText(QCoreApplication.translate("TimeLogDialog", u"Clock Out", None))
        self.edit.setText(QCoreApplication.translate("TimeLogDialog", u"Edit", None))
        self.deleteButton.setText(QCoreApplication.translate("TimeLogDialog", u"Delete", None))
        self.close.setText(QCoreApplication.translate("TimeLogDialog", u"Close", None))
    # retranslateUi

