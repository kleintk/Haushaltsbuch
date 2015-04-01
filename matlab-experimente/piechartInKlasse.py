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
        
        meineFigur = plt.figure(1, figsize=(6,6))
        
        ax = plt.axes([0.1, 0.1, 0.8, 0.8])        
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        fracs = [15,30,45, 10]
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']        
        explode = (0, 0.05, 0, 0)
        
        plt.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
        plt.title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
        
        canvas = FigureCanvas(meineFigur)
        return canvas
        
app = QApplication(sys.argv)
hauptfenster = Hauptfenster()
hauptfenster.show()   
app.exec_()