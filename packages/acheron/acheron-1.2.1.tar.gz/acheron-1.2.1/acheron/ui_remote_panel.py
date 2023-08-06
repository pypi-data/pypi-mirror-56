# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remote_panel.ui'
#
# Created: Tue Nov  3 13:36:12 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RemotePanel(object):
    def setupUi(self, RemotePanel):
        RemotePanel.setObjectName("RemotePanel")
        RemotePanel.resize(112, 182)
        self.verticalLayout = QtGui.QVBoxLayout(RemotePanel)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.goToParentButton = QtGui.QPushButton(RemotePanel)
        self.goToParentButton.setObjectName("goToParentButton")
        self.verticalLayout.addWidget(self.goToParentButton)

        self.retranslateUi(RemotePanel)
        QtCore.QMetaObject.connectSlotsByName(RemotePanel)

    def retranslateUi(self, RemotePanel):
        RemotePanel.setWindowTitle(QtGui.QApplication.translate("RemotePanel", "Remote Device Panel", None, QtGui.QApplication.UnicodeUTF8))
        RemotePanel.setTitle(QtGui.QApplication.translate("RemotePanel", "Remote Device", None, QtGui.QApplication.UnicodeUTF8))
        self.goToParentButton.setText(QtGui.QApplication.translate("RemotePanel", "Go To Radio Tab", None, QtGui.QApplication.UnicodeUTF8))

