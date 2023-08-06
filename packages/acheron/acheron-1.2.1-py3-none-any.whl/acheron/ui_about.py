# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Thu Apr 25 13:55:14 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(302, 232)
        self.verticalLayout = QtGui.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.productLabel = QtGui.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.productLabel.setFont(font)
        self.productLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.productLabel.setObjectName("productLabel")
        self.verticalLayout.addWidget(self.productLabel)
        self.companyLabel = QtGui.QLabel(AboutDialog)
        self.companyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.companyLabel.setOpenExternalLinks(True)
        self.companyLabel.setObjectName("companyLabel")
        self.verticalLayout.addWidget(self.companyLabel)
        self.copyrightLabel = QtGui.QLabel(AboutDialog)
        self.copyrightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.copyrightLabel.setObjectName("copyrightLabel")
        self.verticalLayout.addWidget(self.copyrightLabel)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.version = QtGui.QLabel(AboutDialog)
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setObjectName("version")
        self.verticalLayout.addWidget(self.version)
        self.buildDate = QtGui.QLabel(AboutDialog)
        self.buildDate.setAlignment(QtCore.Qt.AlignCenter)
        self.buildDate.setObjectName("buildDate")
        self.verticalLayout.addWidget(self.buildDate)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.libraryVersionsLabel = QtGui.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.libraryVersionsLabel.setFont(font)
        self.libraryVersionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.libraryVersionsLabel.setObjectName("libraryVersionsLabel")
        self.verticalLayout.addWidget(self.libraryVersionsLabel)
        self.libraryVersions = QtGui.QLabel(AboutDialog)
        self.libraryVersions.setObjectName("libraryVersions")
        self.verticalLayout.addWidget(self.libraryVersions)
        spacerItem2 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Acheron", None, QtGui.QApplication.UnicodeUTF8))
        self.productLabel.setText(QtGui.QApplication.translate("AboutDialog", "Acheron", None, QtGui.QApplication.UnicodeUTF8))
        self.companyLabel.setText(QtGui.QApplication.translate("AboutDialog", "by <a href=\"http://suprocktech.com/\">Suprock Technologies</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.copyrightLabel.setText(QtGui.QApplication.translate("AboutDialog", "© 2019", None, QtGui.QApplication.UnicodeUTF8))
        self.version.setText(QtGui.QApplication.translate("AboutDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.buildDate.setText(QtGui.QApplication.translate("AboutDialog", "Build Date", None, QtGui.QApplication.UnicodeUTF8))
        self.libraryVersionsLabel.setText(QtGui.QApplication.translate("AboutDialog", "Libraries", None, QtGui.QApplication.UnicodeUTF8))
        self.libraryVersions.setText(QtGui.QApplication.translate("AboutDialog", "library: version", None, QtGui.QApplication.UnicodeUTF8))

