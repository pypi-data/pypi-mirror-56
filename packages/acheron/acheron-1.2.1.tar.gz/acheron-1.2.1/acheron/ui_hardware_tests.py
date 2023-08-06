# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hardware_tests.ui'
#
# Created: Mon Apr  1 12:24:34 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_HardwareTestDialog(object):
    def setupUi(self, HardwareTestDialog):
        HardwareTestDialog.setObjectName("HardwareTestDialog")
        HardwareTestDialog.resize(754, 426)
        self.verticalLayout = QtGui.QVBoxLayout(HardwareTestDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.testOutput = QtGui.QPlainTextEdit(HardwareTestDialog)
        self.testOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.testOutput.setReadOnly(True)
        self.testOutput.setObjectName("testOutput")
        self.verticalLayout.addWidget(self.testOutput)
        self.buttonBox = QtGui.QDialogButtonBox(HardwareTestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HardwareTestDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), HardwareTestDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), HardwareTestDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HardwareTestDialog)

    def retranslateUi(self, HardwareTestDialog):
        HardwareTestDialog.setWindowTitle(QtGui.QApplication.translate("HardwareTestDialog", "Hardware Tests", None, QtGui.QApplication.UnicodeUTF8))

