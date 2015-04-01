import sys
from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib
matplotlib.use('Qt4Agg')
# wichtigste zeile!
matplotlib.rcParams['backend.qt4']='PySide'
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure




class Hauptfenster(QMainWindow):
     
    def __init__(self, parent = None):
        super(Hauptfenster, self).__init__()
        canvas = self.canvas_bauen()
        self.setCentralWidget(canvas)
        
    def canvas_bauen(self):
        # generate the plot
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot([0,1])
        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        return canvas
        
app = QApplication(sys.argv)
hauptfenster = Hauptfenster()
hauptfenster.show()   
app.exec_()