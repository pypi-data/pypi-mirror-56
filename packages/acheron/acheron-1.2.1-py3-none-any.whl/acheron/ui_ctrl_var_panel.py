# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctrl_var_panel.ui'
#
# Created: Wed Sep  2 12:45:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CtrlVarPanel(object):
    def setupUi(self, CtrlVarPanel):
        CtrlVarPanel.setObjectName("CtrlVarPanel")
        CtrlVarPanel.resize(99, 41)
        self.verticalLayout = QtGui.QVBoxLayout(CtrlVarPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ctrlVarLayout = QtGui.QVBoxLayout()
        self.ctrlVarLayout.setObjectName("ctrlVarLayout")
        self.verticalLayout.addLayout(self.ctrlVarLayout)
        spacerItem = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(CtrlVarPanel)
        QtCore.QMetaObject.connectSlotsByName(CtrlVarPanel)

    def retranslateUi(self, CtrlVarPanel):
        CtrlVarPanel.setWindowTitle(QtGui.QApplication.translate("CtrlVarPanel", "Control Variable Panel", None, QtGui.QApplication.UnicodeUTF8))
        CtrlVarPanel.setTitle(QtGui.QApplication.translate("CtrlVarPanel", "Control Variables", None, QtGui.QApplication.UnicodeUTF8))

