# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ctrl_var_widget.ui'
#
# Created: Wed Sep  2 12:45:30 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CtrlVarWidget(object):
    def setupUi(self, CtrlVarWidget):
        CtrlVarWidget.setObjectName("CtrlVarWidget")
        CtrlVarWidget.resize(121, 19)
        self.horizontalLayout = QtGui.QHBoxLayout(CtrlVarWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameLabel = QtGui.QLabel(CtrlVarWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.horizontalLayout.addWidget(self.nameLabel)
        self.slider = QtGui.QSlider(CtrlVarWidget)
        self.slider.setMinimumSize(QtCore.QSize(50, 0))
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)

        self.retranslateUi(CtrlVarWidget)
        QtCore.QMetaObject.connectSlotsByName(CtrlVarWidget)

    def retranslateUi(self, CtrlVarWidget):
        CtrlVarWidget.setWindowTitle(QtGui.QApplication.translate("CtrlVarWidget", "Ctrl Var Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("CtrlVarWidget", "Ctrl Var Name", None, QtGui.QApplication.UnicodeUTF8))

