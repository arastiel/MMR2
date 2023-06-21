import sys
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class MainWindow(qw.QMainWindow):
    def __init__(self):
        qw.QMainWindow.__init__(self)
        self.width = 800
        self.height = 800
        self.setWindowTitle("B-Spline")

        #init canvas
        self.canvas_label = qw.QLabel()
        self.canvas = qg.QPixmap(self.width, self.height)

        painter = qg.QPainter(self.canvas)
        painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        painter.end()

        self.canvas_label.setPixmap(self.canvas)

        #start bspline
        self.startCalc = qw.QPushButton("Get bspline")
        self.startCalc.clicked.connect(self.calc_bspline)

        #reset bspline
        self.resetCalc = qw.QPushButton("Reset bspline")
        self.resetCalc.clicked.connect(self.reset_bspline)

        #centered layout for canvas+buttons
        self.centLay = qw.QVBoxLayout()
        self.centLay.addWidget(self.canvas_label)
        self.centLay.addWidget(self.startCalc)
        self.centLay.addWidget(self.resetCalc)

        self.centWid = qw.QWidget()
        self.centWid.setLayout(self.centLay)

        self.setCentralWidget(self.centWid)

        #init control points
        self.ctr = []

        #mouse input as control points
        self.mouse_input()

        self.show()

    def mouse_input(self):
        self.canvas_label.mousePressEvent = self.draw_points

    def draw_points(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.statusBar().showMessage("Position(" + str(round(x)) + " | " + str(round(y)) +
                                     ")",
                                     1000000)

        #init painter
        self.color = qg.QColor(qc.Qt.blue)
        painter = qg.QPainter(self.canvas)
        painter.setPen(qg.QPen(qc.Qt.black, 2, qc.Qt.SolidLine))
        painter.setBrush(qg.QBrush(qc.Qt.red, qc.Qt.SolidPattern))

        # draw point
        painter.drawEllipse(int(x), int(y), 10, 10)
        painter.end()

        # refresh image
        self.canvas_label.setPixmap(self.canvas)
        self.ctr.append([x, y])


    def calc_bspline(self):
        if len(self.ctr) < 4:
            return

        #turn into np for easy slicing
        self.ctr = np.array(self.ctr)
        x = self.ctr[:, 0]
        y = self.ctr[:, 1]

        k = len(x)

        t = np.linspace(2, k-2, 1000, endpoint=True)

        #inits for calculated x/y
        curr_x = 0
        curr_y = 0
        final_x = []
        final_y = []

        for i in t:
            for m in range(k):
                curr_x += x[m] * (0.564 * np.exp(-(i-m)**2))
                curr_y += y[m] * (0.564 * np.exp(-(i-m)**2))
            final_x.append(curr_x)
            final_y.append(curr_y)
            curr_x = 0
            curr_y = 0

        painter = qg.QPainter(self.canvas)
        painter.setPen(qg.QPen(self.color, 2, qc.Qt.SolidLine))

        for i in range(len(final_x)):
            painter.drawPoint(final_x[i], final_y[i])

        painter.end()

        # refresh image
        self.canvas_label.setPixmap(self.canvas)

    def reset_bspline(self):
        painter = qg.QPainter(self.canvas)
        painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        painter.end()

        self.canvas_label.setPixmap(self.canvas)
        self.ctr = []




# Start app
if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    MW = MainWindow()
    sys.exit(app.exec_())
