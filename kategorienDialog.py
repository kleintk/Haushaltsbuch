# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\kategorienDialog.ui'
#
# Created: Tue Apr 22 14:45:33 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_kategorienDialog(object):
    def setupUi(self, kategorienDialog):
        kategorienDialog.setObjectName("kategorienDialog")
        kategorienDialog.resize(433, 388)
        self.buttonBox = QtGui.QDialogButtonBox(kategorienDialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.listWidget = QtGui.QListWidget(kategorienDialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 391, 151))
        self.listWidget.setObjectName("listWidget")
        self.label = QtGui.QLabel(kategorienDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label.setObjectName("label")
        self.groupBox = QtGui.QGroupBox(kategorienDialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 230, 391, 80))
        self.groupBox.setObjectName("groupBox")
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 131, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 51, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(160, 50, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(160, 30, 41, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(300, 50, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(kategorienDialog)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 200, 20, 20))
        self.pushButton_2.setStyleSheet("color: red")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(kategorienDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), kategorienDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), kategorienDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(kategorienDialog)

    def retranslateUi(self, kategorienDialog):
        kategorienDialog.setWindowTitle(QtGui.QApplication.translate("kategorienDialog", "Kategorien verwalten", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("kategorienDialog", "Kategorien:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("kategorienDialog", "Neue Kategorie", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("kategorienDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("kategorienDialog", "Ausgabe", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("kategorienDialog", "Einnahme", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("kategorienDialog", "Typ:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("kategorienDialog", "Hinzufügen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setToolTip(QtGui.QApplication.translate("kategorienDialog", "Ausgewählte Kategorie löschen.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setStatusTip(QtGui.QApplication.translate("kategorienDialog", "Ausgewählte Kategorie löschen.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("kategorienDialog", "X", None, QtGui.QApplication.UnicodeUTF8))

