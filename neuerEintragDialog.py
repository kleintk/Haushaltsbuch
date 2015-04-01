# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\neuerEintragDialog.ui'
#
# Created: Tue Apr 22 11:01:53 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_neuerEintragDialog(object):
    def setupUi(self, neuerEintragDialog):
        neuerEintragDialog.setObjectName("neuerEintragDialog")
        neuerEintragDialog.resize(435, 389)
        self.buttonBox = QtGui.QDialogButtonBox(neuerEintragDialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(neuerEintragDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 41, 16))
        self.label.setObjectName("label")
        self.calendarWidgetDatum = QtGui.QCalendarWidget(neuerEintragDialog)
        self.calendarWidgetDatum.setGeometry(QtCore.QRect(20, 40, 216, 155))
        self.calendarWidgetDatum.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidgetDatum.setGridVisible(False)
        self.calendarWidgetDatum.setNavigationBarVisible(True)
        self.calendarWidgetDatum.setDateEditEnabled(True)
        self.calendarWidgetDatum.setObjectName("calendarWidgetDatum")
        self.label_3 = QtGui.QLabel(neuerEintragDialog)
        self.label_3.setGeometry(QtCore.QRect(260, 20, 51, 16))
        self.label_3.setObjectName("label_3")
        self.comboBoxKategorie = QtGui.QComboBox(neuerEintragDialog)
        self.comboBoxKategorie.setGeometry(QtCore.QRect(260, 40, 141, 22))
        self.comboBoxKategorie.setObjectName("comboBoxKategorie")
        self.label_4 = QtGui.QLabel(neuerEintragDialog)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 71, 16))
        self.label_4.setObjectName("label_4")
        self.lineEditBetrag = QtGui.QLineEdit(neuerEintragDialog)
        self.lineEditBetrag.setGeometry(QtCore.QRect(260, 180, 141, 20))
        self.lineEditBetrag.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditBetrag.setObjectName("lineEditBetrag")
        self.label_5 = QtGui.QLabel(neuerEintragDialog)
        self.label_5.setGeometry(QtCore.QRect(260, 160, 46, 13))
        self.label_5.setObjectName("label_5")
        self.plainTextEdit = QtGui.QPlainTextEdit(neuerEintragDialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 260, 391, 71))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(neuerEintragDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), neuerEintragDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), neuerEintragDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(neuerEintragDialog)

    def retranslateUi(self, neuerEintragDialog):
        neuerEintragDialog.setWindowTitle(QtGui.QApplication.translate("neuerEintragDialog", "Neuer Eintrag", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("neuerEintragDialog", "Datum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("neuerEintragDialog", "Kategorie:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("neuerEintragDialog", "Beschreibung:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("neuerEintragDialog", "Betrag:", None, QtGui.QApplication.UnicodeUTF8))

