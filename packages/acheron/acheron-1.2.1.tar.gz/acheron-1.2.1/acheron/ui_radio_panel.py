# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radio_panel.ui'
#
# Created: Fri Aug  9 09:27:56 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RadioPanel(object):
    def setupUi(self, RadioPanel):
        RadioPanel.setObjectName("RadioPanel")
        RadioPanel.resize(115, 445)
        self.verticalLayout = QtGui.QVBoxLayout(RadioPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.detailScanButton = QtGui.QPushButton(RadioPanel)
        self.detailScanButton.setObjectName("detailScanButton")
        self.verticalLayout.addWidget(self.detailScanButton)
        self.devicesComboBox = QtGui.QComboBox(RadioPanel)
        self.devicesComboBox.setObjectName("devicesComboBox")
        self.verticalLayout.addWidget(self.devicesComboBox)
        self.scanButton = QtGui.QPushButton(RadioPanel)
        self.scanButton.setObjectName("scanButton")
        self.verticalLayout.addWidget(self.scanButton)
        self.connectButton = QtGui.QPushButton(RadioPanel)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout.addWidget(self.connectButton)
        self.disconnectButton = QtGui.QPushButton(RadioPanel)
        self.disconnectButton.setObjectName("disconnectButton")
        self.verticalLayout.addWidget(self.disconnectButton)
        self.advancedMenuButton = QtGui.QPushButton(RadioPanel)
        self.advancedMenuButton.setObjectName("advancedMenuButton")
        self.verticalLayout.addWidget(self.advancedMenuButton)
        self.ctrlVarLayout = QtGui.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.goToRemoteButton = QtGui.QPushButton(RadioPanel)
        self.goToRemoteButton.setObjectName("goToRemoteButton")
        self.verticalLayout.addWidget(self.goToRemoteButton)
        self.actionConnectAnyBootloader = QtGui.QAction(RadioPanel)
        self.actionConnectAnyBootloader.setObjectName("actionConnectAnyBootloader")
        self.actionConnectSpecificBootloader = QtGui.QAction(RadioPanel)
        self.actionConnectSpecificBootloader.setObjectName("actionConnectSpecificBootloader")
        self.actionBootloaderScan = QtGui.QAction(RadioPanel)
        self.actionBootloaderScan.setObjectName("actionBootloaderScan")
        self.actionConnectNoStreaming = QtGui.QAction(RadioPanel)
        self.actionConnectNoStreaming.setObjectName("actionConnectNoStreaming")
        self.actionBulkClaim = QtGui.QAction(RadioPanel)
        self.actionBulkClaim.setObjectName("actionBulkClaim")
        self.actionBulkUpdateFirmware = QtGui.QAction(RadioPanel)
        self.actionBulkUpdateFirmware.setObjectName("actionBulkUpdateFirmware")

        self.retranslateUi(RadioPanel)
        QtCore.QMetaObject.connectSlotsByName(RadioPanel)

    def retranslateUi(self, RadioPanel):
        RadioPanel.setWindowTitle(QtGui.QApplication.translate("RadioPanel", "Radio Panel", None, QtGui.QApplication.UnicodeUTF8))
        RadioPanel.setTitle(QtGui.QApplication.translate("RadioPanel", "Radio", None, QtGui.QApplication.UnicodeUTF8))
        self.detailScanButton.setText(QtGui.QApplication.translate("RadioPanel", "Detail Scan...", None, QtGui.QApplication.UnicodeUTF8))
        self.scanButton.setText(QtGui.QApplication.translate("RadioPanel", "Quick Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.connectButton.setText(QtGui.QApplication.translate("RadioPanel", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectButton.setText(QtGui.QApplication.translate("RadioPanel", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.advancedMenuButton.setText(QtGui.QApplication.translate("RadioPanel", "Advanced Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.goToRemoteButton.setText(QtGui.QApplication.translate("RadioPanel", "Go To Remote Tab", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnectAnyBootloader.setText(QtGui.QApplication.translate("RadioPanel", "Connect Any Bootloader", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnectSpecificBootloader.setText(QtGui.QApplication.translate("RadioPanel", "Connect Specific Bootloader", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBootloaderScan.setText(QtGui.QApplication.translate("RadioPanel", "Bootloader Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnectNoStreaming.setText(QtGui.QApplication.translate("RadioPanel", "Connect (No Streaming)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBulkClaim.setText(QtGui.QApplication.translate("RadioPanel", "Bulk Claim", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBulkClaim.setToolTip(QtGui.QApplication.translate("RadioPanel", "Bulk Claim", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBulkUpdateFirmware.setText(QtGui.QApplication.translate("RadioPanel", "Bulk Update Firmware", None, QtGui.QApplication.UnicodeUTF8))

