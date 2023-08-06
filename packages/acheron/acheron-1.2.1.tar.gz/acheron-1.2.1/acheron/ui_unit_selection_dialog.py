# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_selection_dialog.ui'
#
# Created: Fri Oct 11 16:08:11 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_UnitSelectionDialog(object):
    def setupUi(self, UnitSelectionDialog):
        UnitSelectionDialog.setObjectName("UnitSelectionDialog")
        UnitSelectionDialog.resize(184, 68)
        self.verticalLayout = QtGui.QVBoxLayout(UnitSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.unitGridLayout = QtGui.QGridLayout()
        self.unitGridLayout.setHorizontalSpacing(20)
        self.unitGridLayout.setObjectName("unitGridLayout")
        self.metricLabel = QtGui.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.metricLabel.setFont(font)
        self.metricLabel.setObjectName("metricLabel")
        self.unitGridLayout.addWidget(self.metricLabel, 0, 0, 1, 1)
        self.usLabel = QtGui.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.usLabel.setFont(font)
        self.usLabel.setObjectName("usLabel")
        self.unitGridLayout.addWidget(self.usLabel, 0, 1, 1, 1)
        self.otherLabel = QtGui.QLabel(UnitSelectionDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.otherLabel.setFont(font)
        self.otherLabel.setObjectName("otherLabel")
        self.unitGridLayout.addWidget(self.otherLabel, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.unitGridLayout)
        spacerItem = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(UnitSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(UnitSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), UnitSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), UnitSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UnitSelectionDialog)

    def retranslateUi(self, UnitSelectionDialog):
        UnitSelectionDialog.setWindowTitle(QtGui.QApplication.translate("UnitSelectionDialog", "Select Unit", None, QtGui.QApplication.UnicodeUTF8))
        self.metricLabel.setText(QtGui.QApplication.translate("UnitSelectionDialog", "SI", None, QtGui.QApplication.UnicodeUTF8))
        self.usLabel.setText(QtGui.QApplication.translate("UnitSelectionDialog", "US Customary", None, QtGui.QApplication.UnicodeUTF8))
        self.otherLabel.setText(QtGui.QApplication.translate("UnitSelectionDialog", "Other", None, QtGui.QApplication.UnicodeUTF8))

