# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DateTimeEditDialog.ui'
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


class Ui_DateTimeEditDialog(object):
    def setupUi(self, DateTimeEditDialog):
        if DateTimeEditDialog.objectName():
            DateTimeEditDialog.setObjectName(u"DateTimeEditDialog")
        DateTimeEditDialog.resize(220, 100)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DateTimeEditDialog.sizePolicy().hasHeightForWidth())
        DateTimeEditDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(DateTimeEditDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 60, 201, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.dateTimeEdit = QDateTimeEdit(DateTimeEditDialog)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(10, 30, 201, 22))
        self.dateTimeEdit.setCalendarPopup(True)
        self.label = QLabel(DateTimeEditDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 201, 16))

        self.retranslateUi(DateTimeEditDialog)
        self.buttonBox.accepted.connect(DateTimeEditDialog.accept)
        self.buttonBox.rejected.connect(DateTimeEditDialog.reject)

        QMetaObject.connectSlotsByName(DateTimeEditDialog)
    # setupUi

    def retranslateUi(self, DateTimeEditDialog):
        DateTimeEditDialog.setWindowTitle(QCoreApplication.translate("DateTimeEditDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("DateTimeEditDialog", u"TextLabel", None))
    # retranslateUi

