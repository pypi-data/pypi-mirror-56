# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'change_stream_dialog.ui'
#
# Created: Wed Jul  6 13:03:22 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ChangeStreamDialog(object):
    def setupUi(self, ChangeStreamDialog):
        ChangeStreamDialog.setObjectName("ChangeStreamDialog")
        ChangeStreamDialog.resize(403, 49)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ChangeStreamDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeStreamDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ChangeStreamDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ChangeStreamDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ChangeStreamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeStreamDialog)

    def retranslateUi(self, ChangeStreamDialog):
        ChangeStreamDialog.setWindowTitle(QtGui.QApplication.translate("ChangeStreamDialog", "Change Streams", None, QtGui.QApplication.UnicodeUTF8))

