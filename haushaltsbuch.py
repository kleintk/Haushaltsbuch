# -*- coding: utf-8 -*-


"""
TO DO:
- on delete cascade von kategorien!!!


# Do this instead
t = ('IBM',)
c.execute('select * from stocks where symbol=?', t)

# Larger example
for t in [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
          ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
          ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
         ]:
    c.execute('insert into stocks values (?,?,?,?,?)', t)
"""
import sqlite3
from PySide.QtCore import *
from PySide.QtGui import *
import sys
import os
import hauptfenster
import neuerEintragDialog
import kategorienDialog
import auswertungDialogGui

# matplotlib Imports
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'
# import pylab
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


# noinspection PyUnresolvedReferences,PyBroadException
class Hauptfenster(QMainWindow, hauptfenster.Ui_hauptfensterObjekt):
    def __init__(self, parent=None):
        super(Hauptfenster, self).__init__(parent)
        self.setupUi(self)

        # Buttons und sonstiges Klickis connecten
        self.pushButton.clicked.connect(self.neuen_eintrag_hinzufuegen_dialog_aufrufen)
        self.actionEintrag_hinzufuegen.triggered.connect(self.neuen_eintrag_hinzufuegen_dialog_aufrufen)
        self.actionNeue_Datenbank_erstellen.triggered.connect(self.neue_datenbank_erstellen)
        self.actionEintrag_loeschen.triggered.connect(self.eintrag_loeschen)
        self.actionBuchung_editieren.triggered.connect(self.eintrag_editieren_dialog_aufrufen)
        self.actionKategorien_verwalten.triggered.connect(self.kategorien_verwalten_dialog_aufrufen)
        self.actionBeenden.triggered.connect(self.beenden)
        self.actionDatenbank_loeschen.triggered.connect(self.datenbank_loeschen)
        self.actionBuchungen_auswerten.triggered.connect(self.auswerten_dialog_aufrufen)

        # Rechtsklick-Menü für tree widget
        self.treeWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        entfernen = QAction(self)
        entfernen.setText("Buchung löschen")
        icon_entfernen = QIcon()
        icon_entfernen.addPixmap(QPixmap(":/icons/b-buchung-loeschen.png"), QIcon.Normal, QIcon.Off)
        entfernen.setIcon(icon_entfernen)
        editieren = QAction(self)
        editieren.setText("Buchung editieren")
        icon_editieren = QIcon()
        icon_editieren.addPixmap(QPixmap(":/icons/b-buchung-editieren.png"), QIcon.Normal, QIcon.Off)
        editieren.setIcon(icon_editieren)
        entfernen.triggered.connect(self.eintrag_loeschen)
        editieren.triggered.connect(self.eintrag_editieren_dialog_aufrufen)
        self.treeWidget.addAction(entfernen)
        self.treeWidget.addAction(editieren)

        self.tree_widget_aktualisieren()
        self.uebersicht_aktualisieren()

    def pruefen_ob_datenbank_existiert(self):
        if os.path.exists("datenbank.db"):
            return True
        else:
            self.statusbar.showMessage("Datenbank nicht gefunden oder existiert nicht.", 3000)
            return False

    def neue_datenbank_erstellen(self):
        # Sicherheitsabfrage
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Neue Datenbank?")
        msg_box.setText("Möchten Sie wirklich eine neue Datenbank erstellen?")
        zusatzinfo = "Hinweis: Dabei wird die alte Datenbank gelöscht!"
        msg_box.setDetailedText(zusatzinfo)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        antwort = msg_box.exec_()
        if antwort == QMessageBox.No:
            return

        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            # Tabellen erstellen
            c.execute('''   CREATE TABLE buchung (
                                    id INTEGER PRIMARY KEY,
                                    datum TEXT,
                                    betrag REAL,
                                    beschreibung TEXT,
                                    kategorie INTEGER
                                    );   ''')
            c.execute('''   CREATE TABLE kategorie (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    typ TEXT
                                    );   ''')

            # Voreingestellte Kategorien erstellen
            c.execute('''   INSERT INTO kategorie VALUES(NULL, 'Lebensmittel', 'Ausgabe')   ''')
            c.execute('''   INSERT INTO kategorie VALUES(NULL, 'Miete', 'Ausgabe')   ''')
            c.execute('''   INSERT INTO kategorie VALUES(NULL, 'Gehalt', 'Einnahme')   ''')
            conn.commit()
            print("Datenbank erfolgreich erstellt.")
        except:
            print("Fehler beim Erstellen der Datenbank.")
        c.close()

    def neuen_eintrag_hinzufuegen_dialog_aufrufen(self):
        if not self.pruefen_ob_datenbank_existiert():
            return
        dialog = NeuerEintragDialog()
        dialog.werte_aus_NeuerEintragDialog[str].connect(self.neuen_eintrag_hinzufuegen)
        if dialog.exec_():
            pass

    def eintrag_editieren_dialog_aufrufen(self):
        if not self.pruefen_ob_datenbank_existiert():
            return

        item = self.treeWidget.currentItem()
        id_code = item.text(5)
        datum = item.text(0)
        typ = item.text(1)
        kategorie = item.text(2)
        beschreibung = item.text(3)
        betrag = item.text(4)
        init_values = {"id": id_code, "datum": datum, "typ": typ, "kategorie": kategorie,
                       "beschreibung": beschreibung, "betrag": betrag}
        dialog = EintragEditierenDialog(init_values)
        dialog.werte_aus_EintragEditierenDialog[str].connect(self.eintrag_editieren)
        if dialog.exec_():
            pass

    def neuen_eintrag_hinzufuegen(self, daten):
        if not self.pruefen_ob_datenbank_existiert():
            return
        daten = daten.split("!!!TRENNER!!!")
        # daten: datum, betrag, beschreibung, kategorie

        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()

        try:
            t = (daten[0], float(daten[1]), daten[2], int(daten[3]))
            c.execute('''   INSERT INTO buchung VALUES(NULL, ?, ?, ? ,?)   ''', t)
            conn.commit()
            self.statusbar.showMessage("Neuer Eintrag erfolgreich erstellt.", 3000)
        except:
            self.statusbar.showMessage("Fehler beim Erstellen eines neuen Eintrags.", 3000)
        c.close()
        self.tree_widget_aktualisieren()
        self.uebersicht_aktualisieren()

    def eintrag_editieren(self, daten):
        if not self.pruefen_ob_datenbank_existiert():
            return
        daten = daten.split("!!!TRENNER!!!")
        # daten: datum, betrag, beschreibung, kategorie, id
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()

        try:
            t = (daten[0], float(daten[1]), daten[2], int(daten[3]), int(daten[4]))
            c.execute(
                '''   UPDATE buchung SET datum = ?, betrag = ?, beschreibung = ?, kategorie = ? WHERE id = ?   ''', t)
            conn.commit()
            self.statusbar.showMessage("Buchung editiert.", 3000)
        except:
            self.statusbar.showMessage("Editieren der Buchung fehlgeschlagen.", 3000)
        c.close()
        self.tree_widget_aktualisieren()
        self.uebersicht_aktualisieren()

    def sortierte_liste_aller_buchungen_erstellen(self):
        if not self.pruefen_ob_datenbank_existiert():
            liste = []
            return liste
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            c.execute('''   SELECT b.id, b.datum, b.betrag, b.beschreibung, b.kategorie, k.name, k.typ
                            FROM buchung b, kategorie k
                            WHERE b.kategorie = k.id  ''')
            # Ergebnis in liste packen, tuppels in listen umwandeln, nach datum sortieren
            liste = []
            for i in c:
                liste.append(list(i))
            for i in liste:
                einzelteile = i[1].split("-")
                i[1] = einzelteile[0] + einzelteile[1] + einzelteile[2]
            liste.sort(key=lambda llii: llii[1], reverse=True)
            for i in liste:
                gesammt = i[1][:4] + "-" + i[1][4:6] + "-" + i[1][6:]
                i[1] = gesammt
            c.close()
            return liste
        except:
            print("Fehler beim Erstellen der sortierten Liste.")
            c.close()

    def tree_widget_aktualisieren(self):
        if not self.pruefen_ob_datenbank_existiert():
            self.treeWidget.clear()
            return
        self.treeWidget.clear()
        try:
            liste = self.sortierte_liste_aller_buchungen_erstellen()
            # vorgaenger_datum = ""
            for row in liste:
                # so kann man es nach tags gruppieren, oben und unten vorgaenger_datum entkommentieren
                # if vorgaenger_datum == row[1]:
                # tmp = QTreeWidgetItem(tmp)
                # else:
                # tmp = QTreeWidgetItem(self.treeWidget)
                # obiges statt das hier:
                tmp = QTreeWidgetItem(self.treeWidget)

                tmp.setText(0, row[1])
                tmp.setText(1, row[6])
                tmp.setText(2, row[5])
                tmp.setText(3, row[3])
                tmp.setText(4, str(row[2]))
                tmp.setText(5, str(row[0]))
                if row[6] == "Ausgabe":
                    tmp.setBackground(1, QBrush(QColor(255, 0, 0, 127)))
                    tmp.setBackground(4, QBrush(QColor(255, 0, 0, 127)))
                if row[6] == "Einnahme":
                    tmp.setBackground(1, QBrush(QColor(0, 255, 0, 127)))
                    tmp.setBackground(4, QBrush(QColor(0, 255, 0, 127)))
                    # vorgaenger_datum = row[1]
                    # self.statusbar.showMessage("Buchungsanzeige erfolgreich aktualisiert.", 3000)
        except:
            pass

    def uebersicht_aktualisieren(self):
        if not self.pruefen_ob_datenbank_existiert():
            self.label_4.setText("0")
            self.label_5.setText("0")
            self.label_6.setText("0")
            self.label_9.setText("0")
            return
        try:
            liste = self.sortierte_liste_aller_buchungen_erstellen()
            einnahmen = 0.0
            ausgaben = 0.0
            for i in liste:
                if i[6] == "Einnahme":
                    einnahmen = round(einnahmen + float(i[2]), 2)
                if i[6] == "Ausgabe":
                    ausgaben = round(ausgaben + float(i[2]), 2)
            ergebnis = einnahmen - ausgaben
            ergebnis = round(ergebnis, 2)
            self.label_4.setText(str(einnahmen))
            self.label_5.setText(str(ausgaben))
            self.label_6.setText(str(ergebnis))
            self.label_9.setText(str(ergebnis))
        except:
            pass

    def eintrag_loeschen(self):
        if not self.pruefen_ob_datenbank_existiert():
            return

        item = self.treeWidget.currentItem()
        if item is None:
            self.statusbar.showMessage("Bitte Buchung zum Löschen auswählen.")
            return
        id_code = item.text(5)

        # Sicherheitsabfrage
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Löschen?")
        msg_box.setText("Buchung wirklich löschen?")
        zusatzinfo = u"Datum: {0}\nTyp: {1}\nKategorie: {2}\nBeschreibung: {3}\nBetrag: {4}".format(item.text(0),
                                                                                                    item.text(1),
                                                                                                    item.text(2),
                                                                                                    item.text(3),
                                                                                                    item.text(4),
                                                                                                    item.text(5))
        msg_box.setDetailedText(zusatzinfo)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        antwort = msg_box.exec_()
        if antwort == QMessageBox.No:
            return

        self.treeWidget.invisibleRootItem().removeChild(item)
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        id_code = (id_code, )
        try:
            c.execute('''   DELETE FROM buchung WHERE id=?   ''', id_code)
            conn.commit()
            self.statusbar.showMessage("Buchung erfolgreich gelöscht.", 3000)
        except:
            self.statusbar.showMessage("Fehler beim Löschen der Buchung.", 3000)
        c.close()
        self.tree_widget_aktualisieren()
        self.uebersicht_aktualisieren()

    def kategorien_verwalten_dialog_aufrufen(self):
        if not self.pruefen_ob_datenbank_existiert():
            return
        dialog = KategorienDialog()
        if dialog.exec_():
            pass

    def beenden(self):
        sys.exit()

    def datenbank_loeschen(self):
        # Sicherheitsabfrage
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Datenbank löschen?")
        msg_box.setText("Möchten Sie wirklich die aktuelle Datenbank löschen?")
        zusatzinfo = "Hinweis: Dabei werden alle vorhandenen Daten gelöscht!"
        msg_box.setDetailedText(zusatzinfo)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        antwort = msg_box.exec_()
        if antwort == QMessageBox.No:
            return

        try:
            os.remove("datenbank.db")
            self.tree_widget_aktualisieren()
            self.uebersicht_aktualisieren()
            self.statusbar.showMessage("Datenbank gelöscht.", 3000)
        except:
            self.tree_widget_aktualisieren()
            self.uebersicht_aktualisieren()
            self.statusbar.showMessage("Löschen der Datenbank fehlgeschlagen, keine Rechte?.", 3000)

    def auswerten_dialog_aufrufen(self):
        if not self.pruefen_ob_datenbank_existiert():
            return
        dialog = AuswertenDialog()
        if dialog.exec_():
            pass


# noinspection PyBroadException,PyUnresolvedReferences
class NeuerEintragDialog(QDialog, neuerEintragDialog.Ui_neuerEintragDialog):
    werte_aus_NeuerEintragDialog = Signal(str)

    def __init__(self, parent=None):
        super(NeuerEintragDialog, self).__init__(parent)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.ok_geklickt)
        self.lineEditBetrag.setText("0.00")
        self.kategorie_box_initialisieren()

    def kategorie_box_initialisieren(self):
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()

        try:
            c.execute('''   SELECT name, typ FROM kategorie  ''')
            for row in c:
                if row[1] == "Ausgabe":
                    beschriftung = " - " + row[0]
                    self.comboBoxKategorie.addItem(beschriftung)
                if row[1] == "Einnahme":
                    beschriftung = " + " + row[0]
                    self.comboBoxKategorie.addItem(beschriftung)
        except:
            print("Fehler beim Initialisieren der KategorieBox.")
        c.close()

    def ok_geklickt(self):
        datum = self.calendarWidgetDatum.selectedDate().toPython()

        kategorie = self.comboBoxKategorie.currentText()
        kategorie = kategorie[3:]
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            t = (kategorie, )
            c.execute('''   SELECT id FROM kategorie WHERE name=?  ''', t)
            for row in c:
                kategorie = row[0]
        except:
            print("Fehler beim finden der ID der Kategorie.")
        c.close()

        beschreibung = self.plainTextEdit.toPlainText()
        betrag = self.lineEditBetrag.text()
        betrag = betrag.replace(',', '.')
        daten = u"{0}!!!TRENNER!!!{1}!!!TRENNER!!!{2}!!!TRENNER!!!{3}".format(str(datum), str(betrag),
                                                                              str(beschreibung), str(kategorie))
        self.werte_aus_NeuerEintragDialog.emit(daten)


# noinspection PyBroadException,PyUnresolvedReferences
class EintragEditierenDialog(QDialog, neuerEintragDialog.Ui_neuerEintragDialog):
    werte_aus_EintragEditierenDialog = Signal(str)
    hilfsvariable_index_des_init_values_kategorie = 0
    id_der_buchung = 0

    def __init__(self, init_values, parent=None):
        super(EintragEditierenDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Buchung editieren")
        self.id_der_buchung = init_values["id"]

        self.buttonBox.accepted.connect(self.ok_geklickt)
        self.kategorie_box_initialisieren(init_values)

        # alle werte aus den init_values eintragen:
        datum = init_values["datum"].split("-")
        self.calendarWidgetDatum.setSelectedDate(QDate(int(datum[0]), int(datum[1]), int(datum[2])))
        self.plainTextEdit.setPlainText(init_values["beschreibung"])
        self.lineEditBetrag.setText(init_values["betrag"])
        self.comboBoxKategorie.setCurrentIndex(self.hilfsvariable_index_des_init_values_kategorie)

    def kategorie_box_initialisieren(self, init_values):
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()

        try:
            c.execute('''   SELECT name, typ FROM kategorie  ''')
            zaehler = 0
            for row in c:
                if row[0] == init_values["kategorie"]:
                    self.hilfsvariable_index_des_init_values_kategorie = zaehler
                if row[1] == "Ausgabe":
                    beschriftung = " - " + row[0]
                    self.comboBoxKategorie.addItem(beschriftung)
                if row[1] == "Einnahme":
                    beschriftung = " + " + row[0]
                    self.comboBoxKategorie.addItem(beschriftung)
                zaehler += 1
        except:
            print("Fehler beim Initialisieren der KategorieBox.")
        c.close()

    def ok_geklickt(self):
        datum = self.calendarWidgetDatum.selectedDate().toPython()

        kategorie = self.comboBoxKategorie.currentText()
        kategorie = kategorie[3:]
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            t = (kategorie, )
            c.execute('''   SELECT id FROM kategorie WHERE name=?  ''', t)
            for row in c:
                kategorie = row[0]
        except:
            print("Fehler beim finden der ID der Kategorie.")
        c.close()

        beschreibung = self.plainTextEdit.toPlainText()
        betrag = self.lineEditBetrag.text()
        betrag = betrag.replace(',', '.')
        daten = u"{0}!!!TRENNER!!!{1}!!!TRENNER!!!{2}!!!TRENNER!!!{3}!!!TRENNER!!!{4}".format(str(datum), str(betrag),
                                                                                              str(beschreibung),
                                                                                              str(kategorie),
                                                                                              str(self.id_der_buchung))
        self.werte_aus_EintragEditierenDialog.emit(daten)


# noinspection PyUnresolvedReferences,PyBroadException
class KategorienDialog(QDialog, kategorienDialog.Ui_kategorienDialog):
    def __init__(self, parent=None):
        super(KategorienDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.kategorie_loeschen)
        self.pushButton.clicked.connect(self.kategorie_hinzufuegen)

        # Rechtsklick-Menü für tree widget
        self.listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        entfernen = QAction(self)
        entfernen.setText("Kategorie löschen")
        entfernen_kategorie_icon = QIcon()
        entfernen_kategorie_icon.addPixmap(QPixmap(":/icons/b-kategorien-entfernen.png"), QIcon.Normal, QIcon.Off)
        entfernen.setIcon(entfernen_kategorie_icon)
        entfernen.triggered.connect(self.kategorie_loeschen)
        self.listWidget.addAction(entfernen)

        self.kategorienuebersicht_aktualisieren()

    def kategorienuebersicht_aktualisieren(self):
        self.listWidget.clear()
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            c.execute('''   SELECT id, name, typ FROM kategorie   ''')
            liste = []
            for i in c:
                liste.append(list(i))
            for item in liste:
                tmp = QListWidgetItem(self.listWidget)
                beschriftung = str(item[0]) + ": " + item[1]
                tmp.setText(beschriftung)
                if item[2] == "Einnahme":
                    tmp.setBackground(QBrush(QColor(0, 255, 0, 127)))
                if item[2] == "Ausgabe":
                    tmp.setBackground(QBrush(QColor(255, 0, 0, 127)))
                self.listWidget.addItem(tmp)

                # print("Kategorienuebersicht erfolgreich aktualisiert.")
        except:
            print("Fehler beim Aktualisieren Kategorienuebersicht.")
        c.close()

    def kategorie_loeschen(self):
        item = self.listWidget.currentItem()
        if item is None:
            return

        # Sicherheitsabfrage
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Kategorie löschen?")
        msg_box.setText("Möchten Sie die Kategorie wirklich löschen?")
        zusatzinfo = "Hinweis: Die kann Löschungen von Buchungen nach sich ziehen!"
        msg_box.setDetailedText(zusatzinfo)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        antwort = msg_box.exec_()
        if antwort == QMessageBox.No:
            return

        if item is None:
            print("nix ausgewählt")
        else:
            beschriftung = item.text()
            id_code = beschriftung.split(":")[0]
            conn = sqlite3.connect("datenbank.db")
            c = conn.cursor()
            id_code = (id_code, )
            try:
                c.execute('''   DELETE FROM kategorie WHERE id=?   ''', id_code)
                conn.commit()
                # print("Kategorie erfolgreich gelöscht.")
            except:
                print("Fehler beim Löschen der Kategorie.")
            c.close()
            self.kategorienuebersicht_aktualisieren()

    def kategorie_hinzufuegen(self):
        namen = self.lineEdit.text()
        typ = self.comboBox.currentText()
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        t = (namen, typ, )
        try:
            c.execute('''   INSERT INTO kategorie VALUES(NULL, ?, ?)   ''', t)
            conn.commit()
            # print("Kategorie erfolgreich erstellt.")
        except:
            print("Fehler beim Erstellen der Kategorie.")
        c.close()
        self.kategorienuebersicht_aktualisieren()


# noinspection PyUnresolvedReferences,PyBroadException
class AuswertenDialog(QDialog, auswertungDialogGui.Ui_Dialog):

    def __init__(self, parent=None):
        super(AuswertenDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButtonEA.clicked.connect(self.ea_page_vergleich_anzeigen)
        self.spinBox.valueChanged.connect(self.ea_page_vergleich_anzeigen)
        self.pushButtonEUE.clicked.connect(self.e_page_anzeigen)
        self.spinBox_2.valueChanged.connect(self.e_page_anzeigen)
        self.pushButtonAUE.clicked.connect(self.a_page_anzeigen)
        self.spinBox_3.valueChanged.connect(self.a_page_anzeigen)
        self.pushButtonSchliessen.clicked.connect(self.dialog_schliessen)

        self.layout_framezweipie = QVBoxLayout(self.frameZweiPie)
        self.layout_framezweiverlauf = QVBoxLayout(self.frameZweiVerlauf)
        self.layout_framedreipie = QVBoxLayout(self.frameDreiPie)
        self.layout_framedreiverlauf = QVBoxLayout(self.frameDreiVerlauf)
        self.layout_frameeinsbalken = QVBoxLayout(self.frameEinsBalken)

        # beim oeffnen der Dialogs wird direkt der ea-ergleich angezeigt:
        self.ea_page_vergleich_anzeigen()

    # Buttonfunktionen
    def ea_page_vergleich_anzeigen(self):
        try:
            plt.close('all')
        except:
            print("Fehler beim closen der plt-figures.")
        self.stackedWidget.setCurrentWidget(self.page)
        canvas = self.einnahmen_ausgaben_vergleich_matplotlib_berechnen()

        # entweder die zeile, oder das try-except darunter
        # self.clearLayout(self.layout_text)

        try:
            b = self.layout_frameeinsbalken.takeAt(0)
            b.widget().deleteLater()
        except:
            pass
        self.layout_frameeinsbalken.addWidget(canvas)

    def e_page_anzeigen(self):
        try:
            plt.close('all')
        except:
            print("Fehler beim closen der plt-figures.")
        self.stackedWidget.setCurrentWidget(self.page_2)
        canvas = self.einnahmen_uebersicht_matplotlib_berechnen()

        # entweder die zeile, oder das try-except darunter
        # self.clearLayout(self.layout_text)
        try:
            b = self.layout_framezweipie.takeAt(0)
            b.widget().deleteLater()
            c = self.layout_framezweiverlauf.takeAt(0)
            c.widget().deleteLater()
        except:
            pass
        self.layout_framezweipie.addWidget(canvas[0])
        self.layout_framezweiverlauf.addWidget(canvas[1])

    # tut nicht so wie ich es will, der syntax tut irgendwie: self.clearLayout(self.layout_text)
    def clearlayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

    def a_page_anzeigen(self):
        try:
            plt.close('all')
        except:
            print("Fehler beim closen der plt-figures.")
        self.stackedWidget.setCurrentWidget(self.page_3)
        canvas = self.ausgaben_uebersicht_matplotlib_berechnen()

        # entweder die zeile, oder das try-except darunter
        # self.clearLayout(self.layout_text)
        try:
            b = self.layout_framedreipie.takeAt(0)
            b.widget().deleteLater()
            c = self.layout_framedreiverlauf.takeAt(0)
            c.widget().deleteLater()
        except:
            pass
        self.layout_framedreipie.addWidget(canvas[0])
        self.layout_framedreiverlauf.addWidget(canvas[1])

    def dialog_schliessen(self):
        try:
            plt.close('all')
        except:
            print("Fehler beim closen der plt-figures.")
        self.close()

    # Inhaltsfunktionen
    def einnahmen_ausgaben_vergleich_matplotlib_berechnen(self):
        # Balkendiagramm
        meine_figur = plt.figure(1, facecolor='none')  # , figsize=(6,6)
        meine_figur.clf()
        n_groups = 12
        liste_einnahmen = []
        liste_ausgaben = []

        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            for monat in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                c.execute("""   SELECT sum(b.betrag)
                                FROM buchung b, kategorie k
                                WHERE b.kategorie = k.id
                                AND k.typ = 'Einnahme'
                                AND b.datum >= date('"""+str(self.spinBox.value())+"""-"""+str(monat)+"""-01')
                                AND b.datum <= date('"""+str(self.spinBox.value())+"""-"""+str(monat)+"""-31')   """)
                for wert in c:
                    if wert[0] is None:
                        liste_einnahmen.append(0)
                    else:
                        liste_einnahmen.append(wert[0])

            for monat in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                c.execute("""   SELECT sum(b.betrag)
                                FROM buchung b, kategorie k
                                WHERE b.kategorie = k.id
                                AND k.typ = 'Ausgabe'
                                AND b.datum >= date('"""+str(self.spinBox.value())+"""-"""+str(monat)+"""-01')
                                AND b.datum <= date('"""+str(self.spinBox.value())+"""-"""+str(monat)+"""-31')   """)
                for wert in c:
                    if wert[0] is None:
                        liste_ausgaben.append(0)
                    else:
                        liste_ausgaben.append(wert[0])
        except:
            print("Fehler beim Datenbankenzugriff 1.")
        c.close()

        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        error_config = {'ecolor': '0.3'}
        plt.bar(index, liste_einnahmen, bar_width, alpha=opacity, color='g', error_kw=error_config,
                label='Einnahmen')
        plt.bar(index + bar_width, liste_ausgaben, bar_width, alpha=opacity, color='r', error_kw=error_config,
                label='Ausgaben')
        # plt.xlabel('Monate')
        plt.ylabel('Euro')
        # plt.title('Einnahmen u. Ausgaben per Monat')
        plt.xticks(index + bar_width, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                       'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'))
        plt.legend()
        canvas_balken = FigureCanvas(meine_figur)

        # Tabelle am unteren Rand fuellen:
        zaehler = 0
        for einnahme in liste_einnahmen:
            new_item_einnahme = QTableWidgetItem(str(einnahme))
            new_item_ausgabe = QTableWidgetItem(str(liste_ausgaben[zaehler]))
            differenz = round(einnahme - liste_ausgaben[zaehler], 2)
            new_item_differenz = QTableWidgetItem(str(differenz))
            self.tableWidget.setItem(0, zaehler, new_item_einnahme)
            self.tableWidget.setItem(1, zaehler, new_item_ausgabe)
            self.tableWidget.setItem(2, zaehler, new_item_differenz)
            zaehler += 1
        return canvas_balken

    def einnahmen_uebersicht_matplotlib_berechnen(self):
        # Piechart
        meine_figur = plt.figure(1, figsize=(6, 6), facecolor='none')
        meine_figur.clf()
        plt.axes([0.1, 0.1, 0.8, 0.8])

        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        labels = []
        fracs = []
        legend_text = []
        try:
            c.execute("""   SELECT k.name, sum(b.betrag)
                            FROM buchung b, kategorie k
                            WHERE b.datum >= date('"""+str(self.spinBox_2.value())+"""-01-01')
                            AND b.datum <= date('"""+str(self.spinBox_2.value())+"""-12-31')
                            AND b.kategorie = k.id
                            AND k.typ = 'Einnahme'
                            group by k.name   """)

            for row in c:
                labels.append(row[0])
                fracs.append(row[1])
                legend_text.append("{}:  {:.2f}".format(row[0], row[1]))  # naja
        except:
            print("Fehler beim Datenbankenzugriff 1.")
        c.close()

        # labels = ['Nix', 'Garnix', 'Wenig', 'Bissle']
        # fracs = [15, 30, 45, 10]

        plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
        plt.legend(legend_text, loc='best')
        canvas_piechart = FigureCanvas(meine_figur)

        # Tabelle unten
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            c.execute('''   SELECT id, name
                            FROM kategorie
                            WHERE typ = 'Einnahme'   ''')
            gesammt_liste = []
            liste_id_name = []
            for i in c:
                liste_id_name.append(i)
            zaehler = 0
            for row in liste_id_name:
                gesammt_liste.append([row[1]])

                for monat in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                    c.execute("""   SELECT sum(betrag)
                                    FROM buchung
                                    WHERE kategorie = '"""+str(row[0])+"""'
                                    AND datum >= date('"""+str(self.spinBox_2.value())+"""-"""+str(monat)+"""-01')
                                    AND datum <= date('"""+str(self.spinBox_2.value())+"""-"""+str(monat)+"""-31')
                                    """)
                    for i in c:
                        if i[0] is None:
                            gesammt_liste[zaehler].append(0)
                        else:
                            gesammt_liste[zaehler].append(i[0])
                zaehler += 1
        except:
            print("Fehler beim Datenbankenzugriff 2.")
            gesammt_liste = []
        c.close()

        self.tableWidget_2.setRowCount(len(gesammt_liste))
        zaehler_zeile = 0
        for row in gesammt_liste:
            zaehler_element = 0
            farb_item = QTableWidgetItem()
            farb_item.setBackground(QColor(100, 100, 150))
            self.tableWidget_2.setItem(zaehler_zeile, zaehler_element, farb_item)
            for element in row:
                new_item = QTableWidgetItem(str(element))
                zaehler_element += 1
                self.tableWidget_2.setItem(zaehler_zeile, zaehler_element, new_item)
            zaehler_zeile += 1

        # Verlaufsgrafik
        x_beschriftung = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        x_nummerierung = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # ausgaben = [55, 20, 130, 140, 90, 90, 55, 70, 60, 80, 85, 110]
        # einnahmen = [30, 55, 76, 56, 44, 90, 78, 90, 90, 110, 30, 55]
        legend_text = []  # ["diese chart ist", "leider unfug bisher"]

        meine_figur_zwei = plt.figure(facecolor='none')
        meine_figur_zwei.clf()

        for row in gesammt_liste:
            mein_graph = meine_figur_zwei.add_subplot(111)
            mein_graph.plot(x_nummerierung, row[1:], '-o')
            mein_graph.set_xticks(x_nummerierung)
            mein_graph.set_xticklabels(x_beschriftung)
            legend_text.append(row[0])

        plt.legend(legend_text, loc='best')
        canvas_verlaufsgrafik = FigureCanvas(meine_figur_zwei)

        return canvas_piechart, canvas_verlaufsgrafik

    def ausgaben_uebersicht_matplotlib_berechnen(self):
        # Piechart
        meine_figur = plt.figure(1, figsize=(6, 6), facecolor='none')
        meine_figur.clf()
        plt.axes([0.1, 0.1, 0.8, 0.8])

        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        labels = []
        fracs = []
        legend_text = []
        try:
            c.execute("""   SELECT k.name, sum(b.betrag)
                            FROM buchung b, kategorie k
                            WHERE b.datum >= date('"""+str(self.spinBox_3.value())+"""-01-01')
                            AND b.datum <= date('"""+str(self.spinBox_3.value())+"""-12-31')
                            AND b.kategorie = k.id
                            AND k.typ = 'Ausgabe'
                            group by k.name   """)

            for row in c:
                labels.append(row[0])
                fracs.append(row[1])
                legend_text.append("{}:  {:.2f}".format(row[0], row[1]))  # naja
        except:
            print("Fehler beim Datenbankenzugriff 1.")
        c.close()

        # labels = ['Nix', 'Garnix', 'Wenig', 'Bissle']
        # fracs = [15, 30, 45, 10]

        plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
        plt.legend(legend_text, loc='best')
        canvas_piechart = FigureCanvas(meine_figur)

        # Tabelle unten
        conn = sqlite3.connect("datenbank.db")
        c = conn.cursor()
        try:
            c.execute('''   SELECT id, name
                            FROM kategorie
                            WHERE typ = 'Ausgabe'   ''')
            gesammt_liste = []
            liste_id_name = []
            for i in c:
                liste_id_name.append(i)
            zaehler = 0
            for row in liste_id_name:
                gesammt_liste.append([row[1]])

                for monat in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                    c.execute("""   SELECT sum(betrag)
                                    FROM buchung
                                    WHERE kategorie = '"""+str(row[0])+"""'
                                    AND datum >= date('"""+str(self.spinBox_3.value())+"""-"""+str(monat)+"""-01')
                                    AND datum <= date('"""+str(self.spinBox_3.value())+"""-"""+str(monat)+"""-31')
                                    """)
                    for i in c:
                        if i[0] is None:
                            gesammt_liste[zaehler].append(0)
                        else:
                            gesammt_liste[zaehler].append(i[0])
                zaehler += 1
        except:
            print("Fehler beim Datenbankenzugriff 2.")
            gesammt_liste = []
        c.close()

        self.tableWidget_3.setRowCount(len(gesammt_liste))
        zaehler_zeile = 0
        for row in gesammt_liste:
            zaehler_element = 0
            farb_item = QTableWidgetItem()
            farb_item.setBackground(QColor(100, 100, 150))
            self.tableWidget_3.setItem(zaehler_zeile, zaehler_element, farb_item)
            for element in row:
                new_item = QTableWidgetItem(str(element))
                zaehler_element += 1
                self.tableWidget_3.setItem(zaehler_zeile, zaehler_element, new_item)
            zaehler_zeile += 1

        # Verlaufsgrafik
        x_beschriftung = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        x_nummerierung = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # ausgaben = [55, 20, 130, 140, 90, 90, 55, 70, 60, 80, 85, 110]
        # einnahmen = [30, 55, 76, 56, 44, 90, 78, 90, 90, 110, 30, 55]
        legend_text = []  # ["diese chart ist", "leider unfug bisher"]

        meine_figur_zwei = plt.figure(facecolor='none')
        meine_figur_zwei.clf()

        for row in gesammt_liste:
            mein_graph = meine_figur_zwei.add_subplot(111)
            mein_graph.plot(x_nummerierung, row[1:], '-o')
            mein_graph.set_xticks(x_nummerierung)
            mein_graph.set_xticklabels(x_beschriftung)
            legend_text.append(row[0])

        plt.legend(legend_text, loc='best')
        canvas_verlaufsgrafik = FigureCanvas(meine_figur_zwei)

        return canvas_piechart, canvas_verlaufsgrafik


app = QApplication(sys.argv)
form = Hauptfenster()
form.show()
app.exec_()