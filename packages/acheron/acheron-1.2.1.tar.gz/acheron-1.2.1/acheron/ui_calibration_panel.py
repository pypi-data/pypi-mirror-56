# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calibration_panel.ui'
#
# Created: Tue Oct 15 17:15:15 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CalibrationPanel(object):
    def setupUi(self, CalibrationPanel):
        CalibrationPanel.setObjectName("CalibrationPanel")
        CalibrationPanel.resize(95, 158)
        self.verticalLayout = QtGui.QVBoxLayout(CalibrationPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtGui.QDialogButtonBox(CalibrationPanel)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CalibrationPanel)
        QtCore.QMetaObject.connectSlotsByName(CalibrationPanel)

    def retranslateUi(self, CalibrationPanel):
        CalibrationPanel.setWindowTitle(QtGui.QApplication.translate("CalibrationPanel", "Calibration", None, QtGui.QApplication.UnicodeUTF8))
        CalibrationPanel.setTitle(QtGui.QApplication.translate("CalibrationPanel", "Calibration", None, QtGui.QApplication.UnicodeUTF8))

