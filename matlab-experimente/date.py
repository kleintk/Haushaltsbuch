import sys
from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib
matplotlib.use('Qt4Agg')
# wichtigste zeile!
matplotlib.rcParams['backend.qt4']='PySide'

#import pylab
from pylab import *

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class Hauptfenster(QMainWindow):
     
    def __init__(self, parent = None):
        super(Hauptfenster, self).__init__()
        canvas = self.canvas_bauen()
        self.setCentralWidget(canvas)
        
    def canvas_bauen(self):
        
        x_beschriftung = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        x_nummerierung = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]        
        ausgaben = [55, 20, 130, 140, 90, 90, 55, 70, 60, 80, 85, 110]
        einnahmen = [30, 55, 76, 56, 44, 90, 78, 90, 90, 110, 30, 55]
        legend_text = ["Ausgaben", "Einnahmen"]
        
        meineFigur = plt.figure()
        
        meinGraph = meineFigur.add_subplot(111)        
        meinGraph.plot(x_nummerierung, ausgaben, '-o')        
        meinGraph.set_xticks(x_nummerierung)        
        meinGraph.set_xticklabels(x_beschriftung)
        
        meinGraphZwei = meineFigur.add_subplot(111)        
        meinGraphZwei.plot(x_nummerierung, einnahmen, '-o')        
        meinGraphZwei.set_xticks(x_nummerierung)        
        meinGraphZwei.set_xticklabels(x_beschriftung)
        
        plt.legend(legend_text, loc='best')
        
        
        canvas = FigureCanvas(meineFigur)
        return canvas
        
app = QApplication(sys.argv)
hauptfenster = Hauptfenster()
hauptfenster.show()   
app.exec_()