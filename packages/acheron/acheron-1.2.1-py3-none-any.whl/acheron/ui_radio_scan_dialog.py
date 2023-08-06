# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'radio_scan_dialog.ui'
#
# Created: Thu Apr  4 15:14:33 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_RadioScanDialog(object):
    def setupUi(self, RadioScanDialog):
        RadioScanDialog.setObjectName("RadioScanDialog")
        RadioScanDialog.resize(1000, 445)
        self.verticalLayout = QtGui.QVBoxLayout(RadioScanDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtGui.QTableView(RadioScanDialog)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableView.setSortingEnabled(True)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.activeScan = QtGui.QCheckBox(RadioScanDialog)
        self.activeScan.setObjectName("activeScan")
        self.horizontalLayout.addWidget(self.activeScan)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.filterLabel = QtGui.QLabel(RadioScanDialog)
        self.filterLabel.setObjectName("filterLabel")
        self.horizontalLayout.addWidget(self.filterLabel)
        self.filterSlider = QtGui.QSlider(RadioScanDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterSlider.sizePolicy().hasHeightForWidth())
        self.filterSlider.setSizePolicy(sizePolicy)
        self.filterSlider.setMinimumSize(QtCore.QSize(200, 0))
        self.filterSlider.setMinimum(-100)
        self.filterSlider.setMaximum(0)
        self.filterSlider.setOrientation(QtCore.Qt.Horizontal)
        self.filterSlider.setObjectName("filterSlider")
        self.horizontalLayout.addWidget(self.filterSlider)
        self.filterSpinBox = QtGui.QSpinBox(RadioScanDialog)
        self.filterSpinBox.setMinimum(-100)
        self.filterSpinBox.setMaximum(0)
        self.filterSpinBox.setObjectName("filterSpinBox")
        self.horizontalLayout.addWidget(self.filterSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(RadioScanDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RadioScanDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), RadioScanDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), RadioScanDialog.reject)
        QtCore.QObject.connect(self.filterSlider, QtCore.SIGNAL("valueChanged(int)"), self.filterSpinBox.setValue)
        QtCore.QObject.connect(self.filterSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.filterSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(RadioScanDialog)

    def retranslateUi(self, RadioScanDialog):
        RadioScanDialog.setWindowTitle(QtGui.QApplication.translate("RadioScanDialog", "Radio Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.activeScan.setText(QtGui.QApplication.translate("RadioScanDialog", "Active Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.filterLabel.setText(QtGui.QApplication.translate("RadioScanDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.filterSpinBox.setSuffix(QtGui.QApplication.translate("RadioScanDialog", " dBm", None, QtGui.QApplication.UnicodeUTF8))

