# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SalesOrderEntryVerifyDialog.ui'
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


class Ui_SalesOrderEntryVerifyDialog(object):
    def setupUi(self, SalesOrderEntryVerifyDialog):
        if SalesOrderEntryVerifyDialog.objectName():
            SalesOrderEntryVerifyDialog.setObjectName(u"SalesOrderEntryVerifyDialog")
        SalesOrderEntryVerifyDialog.resize(400, 284)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SalesOrderEntryVerifyDialog.sizePolicy().hasHeightForWidth())
        SalesOrderEntryVerifyDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QDialogButtonBox(SalesOrderEntryVerifyDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 240, 361, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.No|QDialogButtonBox.Yes)
        self.label = QLabel(SalesOrderEntryVerifyDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 171, 16))
        self.textBrowser = QTextBrowser(SalesOrderEntryVerifyDialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 30, 361, 181))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy1)
        self.label_2 = QLabel(SalesOrderEntryVerifyDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 220, 151, 16))

        self.retranslateUi(SalesOrderEntryVerifyDialog)
        self.buttonBox.accepted.connect(SalesOrderEntryVerifyDialog.accept)
        self.buttonBox.rejected.connect(SalesOrderEntryVerifyDialog.reject)

        QMetaObject.connectSlotsByName(SalesOrderEntryVerifyDialog)
    # setupUi

    def retranslateUi(self, SalesOrderEntryVerifyDialog):
        SalesOrderEntryVerifyDialog.setWindowTitle(QCoreApplication.translate("SalesOrderEntryVerifyDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("SalesOrderEntryVerifyDialog", u"New Sales Order Details:", None))
        self.label_2.setText(QCoreApplication.translate("SalesOrderEntryVerifyDialog", u"Are these details correct?", None))
    # retranslateUi

