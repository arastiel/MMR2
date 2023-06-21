import sys
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

class Canvas(FigureCanvasQTAgg):
    def __init__(self):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=150)
        self.ax.grid()
        super(Canvas, self).__init__(fig)


class MainWindow(qw.QMainWindow):
    def __init__(self):
        qw.QMainWindow.__init__(self)

        self.sc = Canvas()
        self.toolbar = NavigationToolbar2QT(self.sc, self)

        self.init_window()

        #2.3
        #self.draw_function()
        #self.draw_fft()

        #2.4
        self.draw_2function()
        self.draw_2fft()

        self.show()

    def init_window(self):
        self.width = 800
        self.height = 800
        self.setWindowTitle("MainWindow")

        # Set canvas
        self.canvas_label = qw.QLabel()
        self.canvas = qg.QPixmap(self.width, self.height)

        # init canvas
        painter = qg.QPainter(self.canvas)
        painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        painter.end()

        # set central widget
        plotLayout = qw.QVBoxLayout()
        plotLayout.addWidget(self.toolbar)
        plotLayout.addWidget(self.sc)

        centWidget = qw.QWidget()
        centWidget.setLayout(plotLayout)
        self.setCentralWidget(centWidget)



    def draw_function(self):
        self.t = np.linspace(0, 2*np.pi, 500, endpoint=True)

        #different functions
        #self.y = (self.t**2)
        #self.y = np.cos(self.t)
        #self.y = np.sin(self.t)
        self.y = np.sin(2*np.pi * self.t)*100

        self.sc.ax.plot(self.t, self.y)

    def draw_fft(self):
        lambdaSin = 0
        lambdasSin = []
        lambdaCos = 0
        lambdasCos = []

        for m in range(len(self.t)):
            for i in range(len(self.t)):
                lambdaSin += np.sin(m*self.t[i])*self.y[i]
                lambdaCos += np.cos(m*self.t[i])*self.y[i]

            lambdaSin *= 1/len(self.t) * 2 * np.pi
            lambdasSin.append(lambdaSin)
            lambdaSin = 0

            lambdaCos *= 1/len(self.t) * 2 * np.pi
            lambdasCos.append(lambdaCos)
            lambdaCos = 0

        values = []

        for i in range(len(lambdasSin)):
            ft = lambdasSin[i] * np.sin(i*self.t[i]) + lambdasCos[i] * np.cos(i*self.t[i])
            values.append(ft)

        self.sc.ax.plot(self.t, values)

        '''        
        np fft implementation as comparison        
        out = np.fft.fft(self.y)
        self.sc.ax.plot(self.x, out)
        '''

    def draw_2function(self):
        self.t = np.linspace(0, 2*np.pi, 500, endpoint=True)

        self.xt = self.t*np.cos(self.t)
        self.yt = self.t*np.sin(self.t)

        self.sc.ax.plot(self.xt, self.yt)


    def draw_2fft(self):
        lambdaSinX = 0
        lambdasSinX = []
        lambdaCosX = 0
        lambdasCosX = []

        lambdaSinY = 0
        lambdasSinY = []
        lambdaCosY = 0
        lambdasCosY = []

        for m in range(len(self.t)):
            for i in range(len(self.t)):
                lambdaSinX += np.sin(m*self.t[i])*self.xt[i]
                lambdaCosX += np.cos(m*self.t[i])*self.xt[i]

            lambdaSinX *= 1/len(self.t) * 2 * np.pi
            lambdasSinX.append(lambdaSinX)
            lambdaSinX = 0

            lambdaCosX *= 1/len(self.t) * 2 * np.pi
            lambdasCosX.append(lambdaCosX)
            lambdaCosX = 0

        for m in range(len(self.t)):
            for i in range(len(self.t)):
                lambdaSinY += np.sin(m*self.t[i])*self.yt[i]
                lambdaCosY += np.cos(m*self.t[i])*self.yt[i]

            lambdaSinY *= 1/len(self.t) * 2 * np.pi
            lambdasSinY.append(lambdaSinY)
            lambdaSinY = 0

            lambdaCosY *= 1/len(self.t) * 2 * np.pi
            lambdasCosY.append(lambdaCosY)
            lambdaCosY = 0

        valuesX = []
        valuesY = []

        for i in range(len(lambdasSinX)):
            ftX = lambdasSinX[i] * np.sin(i*self.t[i]) + lambdasCosX[i] * np.cos(i*self.t[i])
            valuesX.append(ftX)
            ftY = lambdasSinY[i] * np.sin(i*self.t[i]) + lambdasCosY[i] * np.cos(i*self.t[i])
            valuesY.append(ftY)

        self.sc.ax.plot(valuesX, valuesY)

        outx = np.fft.ifft(self.xt)
        outy = np.fft.ifft(self.yt)
        self.sc.ax.plot(outx, outy)


# Start app
if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    MW = MainWindow()
    sys.exit(app.exec_())
