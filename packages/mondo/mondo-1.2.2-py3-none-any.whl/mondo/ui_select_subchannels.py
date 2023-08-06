# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_subchannels.ui'
#
# Created: Fri Dec  9 13:24:17 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SelectSubchannelsDialog(object):
    def setupUi(self, SelectSubchannelsDialog):
        SelectSubchannelsDialog.setObjectName("SelectSubchannelsDialog")
        SelectSubchannelsDialog.resize(400, 49)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SelectSubchannelsDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SelectSubchannelsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SelectSubchannelsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SelectSubchannelsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SelectSubchannelsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectSubchannelsDialog)

    def retranslateUi(self, SelectSubchannelsDialog):
        SelectSubchannelsDialog.setWindowTitle(QtGui.QApplication.translate("SelectSubchannelsDialog", "Select Subchannels Channels", None, QtGui.QApplication.UnicodeUTF8))

