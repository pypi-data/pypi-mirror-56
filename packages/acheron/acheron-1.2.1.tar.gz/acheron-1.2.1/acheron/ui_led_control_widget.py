# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'led_control_widget.ui'
#
# Created: Wed Mar 13 16:26:33 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_LEDControlWidget(object):
    def setupUi(self, LEDControlWidget):
        LEDControlWidget.setObjectName("LEDControlWidget")
        LEDControlWidget.resize(176, 20)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(LEDControlWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.slider = QtGui.QSlider(LEDControlWidget)
        self.slider.setMinimumSize(QtCore.QSize(128, 0))
        self.slider.setMaximum(255)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.horizontalLayout_3.addWidget(self.slider)
        self.spinBox = QtGui.QSpinBox(LEDControlWidget)
        self.spinBox.setMaximum(255)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)

        self.retranslateUi(LEDControlWidget)
        QtCore.QObject.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"), self.spinBox.setValue)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.slider.setValue)
        QtCore.QMetaObject.connectSlotsByName(LEDControlWidget)
        LEDControlWidget.setTabOrder(self.slider, self.spinBox)

    def retranslateUi(self, LEDControlWidget):
        LEDControlWidget.setWindowTitle(QtGui.QApplication.translate("LEDControlWidget", "LED Control Widget", None, QtGui.QApplication.UnicodeUTF8))

