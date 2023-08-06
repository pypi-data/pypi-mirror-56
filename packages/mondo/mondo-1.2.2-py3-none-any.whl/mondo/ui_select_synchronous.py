# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_synchronous.ui'
#
# Created: Mon Aug  1 12:44:43 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SelectSynchronousDialog(object):
    def setupUi(self, SelectSynchronousDialog):
        SelectSynchronousDialog.setObjectName("SelectSynchronousDialog")
        SelectSynchronousDialog.resize(400, 49)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SelectSynchronousDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SelectSynchronousDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SelectSynchronousDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SelectSynchronousDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SelectSynchronousDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectSynchronousDialog)

    def retranslateUi(self, SelectSynchronousDialog):
        SelectSynchronousDialog.setWindowTitle(QtGui.QApplication.translate("SelectSynchronousDialog", "Select Synchronous Channels", None, QtGui.QApplication.UnicodeUTF8))

