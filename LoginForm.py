# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginForm.ui'
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


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        if LoginForm.objectName():
            LoginForm.setObjectName(u"LoginForm")
        LoginForm.resize(362, 192)
        self.login = QPushButton(LoginForm)
        self.login.setObjectName(u"login")
        self.login.setGeometry(QRect(180, 150, 75, 23))
        self.login.setAutoDefault(False)
        self.cancel = QPushButton(LoginForm)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setGeometry(QRect(270, 150, 75, 23))
        self.label = QLabel(LoginForm)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 361, 41))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(LoginForm)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 61, 16))
        self.label_3 = QLabel(LoginForm)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 110, 61, 16))
        self.username = QLineEdit(LoginForm)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(80, 70, 261, 20))
        self.username.setClearButtonEnabled(True)
        self.password = QLineEdit(LoginForm)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(80, 110, 261, 20))
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setClearButtonEnabled(True)

        self.retranslateUi(LoginForm)

        self.login.setDefault(True)


        QMetaObject.connectSlotsByName(LoginForm)
    # setupUi

    def retranslateUi(self, LoginForm):
        LoginForm.setWindowTitle(QCoreApplication.translate("LoginForm", u"Form", None))
        self.login.setText(QCoreApplication.translate("LoginForm", u"Login", None))
        self.cancel.setText(QCoreApplication.translate("LoginForm", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("LoginForm", u"Ultimate Controls, LLC. \n"
"Order Management System", None))
        self.label_2.setText(QCoreApplication.translate("LoginForm", u"Username:", None))
        self.label_3.setText(QCoreApplication.translate("LoginForm", u"Password:", None))
    # retranslateUi

