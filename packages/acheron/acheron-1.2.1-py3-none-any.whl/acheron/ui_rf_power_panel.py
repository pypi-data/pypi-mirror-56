# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rf_power_panel.ui'
#
# Created: Wed Sep  2 12:45:35 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RFPowerPanel(object):
    def setupUi(self, RFPowerPanel):
        RFPowerPanel.setObjectName("RFPowerPanel")
        RFPowerPanel.resize(111, 99)
        self.verticalLayout = QtGui.QVBoxLayout(RFPowerPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.enableButton = QtGui.QPushButton(RFPowerPanel)
        self.enableButton.setObjectName("enableButton")
        self.verticalLayout.addWidget(self.enableButton)
        self.disableButton = QtGui.QPushButton(RFPowerPanel)
        self.disableButton.setObjectName("disableButton")
        self.verticalLayout.addWidget(self.disableButton)
        self.ctrlVarLayout = QtGui.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(RFPowerPanel)
        QtCore.QMetaObject.connectSlotsByName(RFPowerPanel)

    def retranslateUi(self, RFPowerPanel):
        RFPowerPanel.setWindowTitle(QtGui.QApplication.translate("RFPowerPanel", "RF Power Panel", None, QtGui.QApplication.UnicodeUTF8))
        RFPowerPanel.setTitle(QtGui.QApplication.translate("RFPowerPanel", "RF Power", None, QtGui.QApplication.UnicodeUTF8))
        self.enableButton.setText(QtGui.QApplication.translate("RFPowerPanel", "Enable RF Power", None, QtGui.QApplication.UnicodeUTF8))
        self.disableButton.setText(QtGui.QApplication.translate("RFPowerPanel", "Disable RF Power", None, QtGui.QApplication.UnicodeUTF8))

