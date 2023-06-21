import sys
import numpy as np
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class MainWindow(qw.QMainWindow):
    def __init__(self):
        qw.QMainWindow.__init__(self)
        self.width = 600
        self.height = 600
        self.setWindowTitle("Budget Paint")

        self.init_paintGUI()
        self.show()
    
    def init_paintGUI(self):
        #init canvas
        self.paint_label = qw.QLabel()
        self.canvas = qg.QPixmap(self.width, self.height)

        painter = qg.QPainter(self.canvas)
        painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        painter.end()

        self.paint_label.setPixmap(self.canvas)

        self.init_toolbar()

        self.cent_lay = qw.QVBoxLayout()
        
        
        self.cent_lay.addWidget(self.paint_label)
        self.cent_lay.addLayout(self.toolbar)
        self.cent_wid = qw.QWidget()
        self.cent_wid.setLayout(self.cent_lay)
        self.setCentralWidget(self.cent_wid)

        self.last_x, self.last_y = None, None
        self.pen_color = qc.Qt.black

    def init_toolbar(self):
        self.toolbar = qw.QVBoxLayout()

        btn_color = qw.QPushButton('Change color', self)
        btn_color.setToolTip('Opens color dialog')
        btn_color.clicked.connect(self.change_color)

        btn_reset = qw.QPushButton('Reset', self)
        btn_reset.setToolTip('Opens color dialog')
        btn_reset.clicked.connect(self.reset_paint)
        
        btn_lay = qw.QHBoxLayout()
        btn_lay.addWidget(btn_color)
        btn_lay.addWidget(btn_reset)
        self.toolbar.addLayout(btn_lay)

        check_lay = qw.QHBoxLayout()
        self.check_rotate = qw.QCheckBox("Rotation")
        self.check_translate = qw.QCheckBox("Translation")
        self.check_mirror = qw.QCheckBox("Mirror")
        mirror_lab = qw.QLabel("Mirror axis:")
        self.check_mirrorX = qw.QCheckBox("MirrorX")
        self.check_mirrorX.setChecked(True)
        self.check_mirrorY = qw.QCheckBox("MirrorY")

        check_lay.addWidget(self.check_rotate)
        check_lay.addWidget(self.check_mirror)
        check_lay.addWidget(self.check_translate)
        check_lay.addWidget(mirror_lab)
        check_lay.addWidget(self.check_mirrorX)
        check_lay.addWidget(self.check_mirrorY)
        self.toolbar.addLayout(check_lay)

        rotation_lay = qw.QHBoxLayout()
        rotation_text = qw.QLabel("rotation amount (k-times): ")
        self.rotation_line = qw.QLineEdit("8")

        rotation_lay.addWidget(rotation_text)
        rotation_lay.addWidget(self.rotation_line)
        self.toolbar.addLayout(rotation_lay)


        translation_lay = qw.QHBoxLayout()
        translation_textX = qw.QLabel("shiftX: ")
        self.translation_lineX = qw.QLineEdit("50")
        translation_textY = qw.QLabel("shiftY: ")
        self.translation_lineY = qw.QLineEdit("50")

        translation_lay.addWidget(translation_textX)
        translation_lay.addWidget(self.translation_lineX)
        translation_lay.addWidget(translation_textY)
        translation_lay.addWidget(self.translation_lineY)

        self.toolbar.addLayout(translation_lay)


    ###-------- toolbar functions --------####
    @qc.pyqtSlot()
    def change_color(self):
        self.openColorDialog()

    def openColorDialog(self):
        color = qw.QColorDialog.getColor()

        if color.isValid():
            self.pen_color = color

    def reset_paint(self):
        painter = qg.QPainter(self.paint_label.pixmap())
        painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        painter.end()
        self.update()
    ###-------- end toolbar functions --------####


    ###-------- mouse events --------####
    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return #first click ignored

        #check drawmode via checkboxes
        self.drawmode = []
        if self.check_rotate.isChecked():
            self.drawmode.append("rotation")
        if self.check_mirror.isChecked():
            self.drawmode.append("mirror")
        if self.check_translate.isChecked():
            self.drawmode.append("translation")

        
        self.pixel_size = 1 / (self.width / 2)

        painter = qg.QPainter(self.paint_label.pixmap())
        painter.setPen(qg.QPen(self.pen_color, 4, qc.Qt.SolidLine))
        painter.drawPoint(self.last_x, self.last_y)

        #draw according to drawmode
        if "rotation" in self.drawmode:
            self.draw_rotated(painter, self.last_x, self.last_y)
        elif "mirror" in self.drawmode:
            self.draw_mirrored(painter, self.last_x, self.last_y)
        elif "translation" in self.drawmode:
            self.draw_translated(painter, self.last_x, self.last_y)
            
        painter.end()
        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
    ###-------- end mouse events --------####    


    ###-------- draw stuff --------####
    def draw_rotated(self, painter, x, y):
        k = int(self.rotation_line.text())

        if k == 0 or k == 1:
            return

        _alpha = 2 * np.pi / k

        x, y = self.convert_xy(x, y)    #convert x,y to coordinate system to fit it into the screen
        old = np.array([x, y])
        
        for i in range(k + 1):
            alpha = _alpha * i
            rot_mat = np.array([[np.cos(alpha), np.sin(alpha)], [-(np.sin(alpha)), np.cos(alpha)]])
            new = np.matmul(rot_mat, old)
            new = self.convert_back_xy(new)
            painter.drawPoint(new[0], new[1])

            if "mirror" in self.drawmode:   #check if other modes are selected
                self.draw_mirrored(painter, new[0], new[1])
            elif "translation" in self.drawmode:
                self.draw_translated(painter, new[0], new[1])


    def draw_translated(self, painter, x, y):
        shift_x = int(self.translation_lineX.text())
        shift_y = int(self.translation_lineY.text())
        if shift_x == 0 and shift_y == 0:
            return
        elif shift_x == 0:
            for j in range(self.paint_label.pixmap().height()//shift_y):
                for k in range(-1, 2, 2):
                    painter.drawPoint(x, y - (shift_y * j * k))
        elif shift_y == 0:
            for i in range(self.paint_label.pixmap().width()//shift_x):
                for k in range(-1, 2, 2):
                    painter.drawPoint(x - (shift_x * i * k), y)
        else:
            for i in range(self.paint_label.pixmap().width()//shift_x):
                for j in range(self.paint_label.pixmap().height()//shift_y):
                    for k in range(-1, 2, 2):
                        painter.drawPoint(x - (shift_x * i * k), y)
                        painter.drawPoint(x - (shift_x * i * k), y - (shift_y * j * k))
                        painter.drawPoint(x + (shift_x * i * k), y - (shift_y * j * k))
                        painter.drawPoint(x, y - (shift_y * j * k))


    def draw_mirrored(self, painter, x, y):
        axis = []
        if self.check_mirrorX.isChecked():
            axis.append("x")
        if self.check_mirrorY.isChecked():
            axis.append("y")

        if len(axis) == 1:
            if "x" in axis:     #case x axis only
                painter.drawPoint(self.width - x, y)
                if "translation" in self.drawmode:
                    self.draw_translated(painter, x, y)
                    self.draw_translated(painter, self.width-x, y)

            if "y" in axis:     #case y axis only
                painter.drawPoint(x, self.height - y)
                if "translation" in self.drawmode:
                    self.draw_translated(painter, x, y)
                    self.draw_translated(painter, x, self.height - y)
       
        if len(axis) == 2:
            if "x" in axis and "y" in axis:     #case x axis and y axis
                painter.drawPoint(self.width - x, y)
                painter.drawPoint(x, self.height - y)
                painter.drawPoint(self.width - x, self.height - y)
                if "translation" in self.drawmode:
                    self.draw_translated(painter, x, y)
                    self.draw_translated(painter, x, self.height - y)
                    self.draw_translated(painter, self.width - x, y)
                    self.draw_translated(painter, self.width - x, self.height - y)

        
    def convert_xy(self, x, y):
        boundary = self.width / 2
        y = self.width - y

        # convert pixel int into a coordinate system
        x = (x - boundary) * self.pixel_size
        y = (boundary - y) * self.pixel_size

        return x, y

    def convert_back_xy(self, xy):
        boundary = self.width / 2

        # convert back to pixel
        if xy[0] >= 0:  # pos[0] = x
            x = boundary - abs(xy[0] / self.pixel_size)
        elif xy[0] < 0:
            x = boundary - (xy[0] / self.pixel_size)
        if xy[1] >= 0:
            y = boundary - (xy[1] / self.pixel_size)
        elif xy[1] < 0:
            y = boundary + abs(xy[1] / self.pixel_size)
        return int(x), int(y)

    ###-------- end draw stuff --------####

if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


