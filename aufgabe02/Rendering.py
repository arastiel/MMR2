from Polygon import Polygon, Object3D
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import time
import numpy as np
import sys

class Window(qw.QMainWindow):
    def __init__(self, object_widget):
        super().__init__()

        self.title = "test"
        self.top = 200
        self.left = 500
        self.width = 1200
        self.height = 1200


        #self.draw_object = draw_object
        self.object_widget = object_widget


        #self.btn_animation = qw.QPushButton("Start Animation", self)
        #self.btn_animation.move(30, 30)
        #self.btn_animation.clicked.connect(self.animate)

        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_widget = qw.QWidget()

        self.x_angle_slider = qw.QSlider(qc.Qt.Horizontal)
        self.x_angle_slider.setMinimum(-360)
        self.x_angle_slider.setMaximum(360)
        self.x_angle_slider.valueChanged.connect(self.change_x_angle)
        self.x_angle_slider.sliderReleased.connect(self.reset_x_angle_slider)

        self.y_angle_slider = qw.QSlider(qc.Qt.Horizontal)
        self.y_angle_slider.setMinimum(-360)
        self.y_angle_slider.setMaximum(360)
        self.y_angle_slider.valueChanged.connect(self.change_y_angle)
        self.y_angle_slider.sliderReleased.connect(self.reset_y_angle_slider)

        self.z_angle_slider = qw.QSlider(qc.Qt.Horizontal)
        self.z_angle_slider.setMinimum(-360)
        self.z_angle_slider.setMaximum(360)
        self.z_angle_slider.valueChanged.connect(self.change_z_angle)
        self.z_angle_slider.sliderReleased.connect(self.reset_z_angle_slider)

        #self.move_x_slider = qw.QSlider(qc.Qt.Horizontal)
        #self.move_x_slider.setMinimum(-10)
        #self.move_x_slider.setMaximum(10)
        #self.move_x_slider.setSliderPosition(0)
        #self.move_x_slider.valueChanged.connect(self.changeX)
        #self.move_x_slider.sliderReleased.connect(self.reset_move_x_slider)

        self.main_layout = qw.QVBoxLayout()
        self.main_layout.addWidget(self.object_widget)
        self.main_layout.addWidget(self.x_angle_slider)
        self.main_layout.addWidget(self.y_angle_slider)
        self.main_layout.addWidget(self.z_angle_slider)
        #self.main_layout.addWidget(self.move_x_slider)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.setContentsMargins(0, 0, 0, 0)

        self.show()

    def change_x_angle(self):
        self.object_widget.x_spin_drawing(self.x_angle_slider.value())

    def reset_x_angle_slider(self):
        self.x_angle_slider.setSliderPosition(0)

    def change_y_angle(self):
        self.object_widget.y_spin_drawing(self.y_angle_slider.value())

    def reset_y_angle_slider(self):
        self.y_angle_slider.setSliderPosition(0)

    def change_z_angle(self):
        self.object_widget.z_spin_drawing(self.z_angle_slider.value())

    def reset_z_angle_slider(self):
        self.z_angle_slider.setSliderPosition(0)



    def changeX(self):
        self.object_widget.move_x_direction(self.move_x_slider.value())

    def reset_move_x_slider(self):
        self.move_x_slider.setSliderPosition(0)

class ObjectWidget(qw.QWidget):
    def __init__(self, draw_object):
        super().__init__()

        self.width = 1200
        self.height = 1200
        self.depth = self.width/100
        self.setGeometry(-self.width, -self.height, self.width, self.height)

        #paint devices
        self.display = qw.QLabel()
        self.canvas = qg.QPixmap(self.width, self.height)
        self.painter = qg.QPainter(self.canvas)
        self.painter.setPen(qg.QPen(qc.Qt.red, 1, qc.Qt.SolidLine))

        #init function
        self.og_draw_object = draw_object
        self.new_x_y_object = self.calc_x_y_object(draw_object)

        #scaling_variables
        self.min_x = self.new_x_y_object.get_min_x()
        self.max_x = self.new_x_y_object.get_max_x()
        self.min_y = self.new_x_y_object.get_min_y()
        self.max_y = self.new_x_y_object.get_max_y()
        self.min_z = self.new_x_y_object.get_min_z()
        self.max_z = self.new_x_y_object.get_max_z()

        self.a = -(self.width*0.9)/(self.min_x-self.max_x)
        self.b = -self.a * self.min_x

        self.c = -(self.height*0.9)/(self.min_y-self.max_y)
        self.d = -self.c * self.min_y

        self.e = -(self.depth)/(self.min_z-self.max_z)
        self.f = -self.e * self.min_z

        #scaling_function
        self.scaled_draw_object = self.scale_draw_object(self.new_x_y_object)

        #draw function
        self.calc_draw_points(self.scaled_draw_object)


        self.main_layout = qw.QHBoxLayout()
        self.main_layout.setAlignment(qc.Qt.AlignCenter)
        self.main_layout.addWidget(self.display)
        self.setLayout(self.main_layout)

        #self.show()

    def calc_x_y_object(self, draw_object):
        draw_object_ = draw_object
        for i in draw_object_.polygon_list:
            i.corners[:, 0] = i.corners[:, 0] + 0.5*np.sqrt(2)*i.corners[:, 2]
            i.corners[:, 1] = i.corners[:, 1] + 0.5*np.sqrt(2)*i.corners[:, 2]
        return draw_object_

    def scale_draw_object(self, draw_object):
        draw_object_ = draw_object
        for i in draw_object_.polygon_list:
            i.corners[:, 0] = self.a * i.corners[:, 0] + self.b
            i.corners[:, 1] = self.c * i.corners[:, 1] + self.d
            i.corners[:, 2] = self.e * i.corners[:, 2] + self.f
        return draw_object_

    def calc_draw_points(self, draw_object):
        sort_points = []
        sorting = []
        draw_points = []

        for i in draw_object.polygon_list:
            sort_points.append(i.corners)

        for i in sort_points:
            sorting.append(np.mean(i[:, 2]))

        sorting__ = np.array([sorting, np.arange(start=0, stop=len(sorting))])
        new_sort = sorting__.transpose()

        sorted_polys = new_sort[new_sort[:, 0].argsort()]

        for i in sorted_polys:
            for j in range(3):
                draw_points.append(qc.QPointF(draw_object.polygon_list[int(i[1])].corners[j][0], draw_object.polygon_list[int(i[1])].corners[j][1]))
            polygon = qg.QPolygonF(draw_points)
            path = qg.QPainterPath()
            path.addPolygon(polygon)
            self.painter.fillPath(path, qg.QColor(draw_object.polygon_list[int(i[1])].rgb[0], draw_object.polygon_list[int(i[1])].rgb[1], draw_object.polygon_list[int(i[1])].rgb[2]))
            self.painter.drawPolygon(polygon)
            draw_points = []

        self.display.setPixmap(self.canvas)
        return

    def x_spin_drawing(self, degree):
        self.canvas.fill(qc.Qt.black)
        degree = degree/720
        b_list = [[1, 0, 0], [0, np.cos(degree), -np.sin(degree)], [0, np.sin(degree), np.cos(degree)]]
        b = np.array(b_list)
        for i in self.scaled_draw_object.polygon_list:
            i.corners[:, 1] = i.corners[:, 1] - self.height*0.9/2
            #i.corners[:, 2] = i.corners[:, 2] + self.depth/2
            i.corners = i.corners.dot(b)
            i.corners[:, 1] = i.corners[:, 1] + self.height*0.9/2
            #i.corners[:, 2] = i.corners[:, 2] - self.depth/2

        self.calc_draw_points(self.scaled_draw_object)

    def y_spin_drawing(self, degree):
        self.canvas.fill(qc.Qt.black)
        degree = degree/720
        b_list = [[np.cos(degree), 0, np.sin(degree)], [0, 1, 0], [-np.sin(degree), 0, np.cos(degree)]]
        b = np.array(b_list)
        for i in self.scaled_draw_object.polygon_list:
            i.corners[:, 0] = i.corners[:, 0] - self.width*0.9/2
            #i.corners[:, 2] = i.corners[:, 2] + self.depth/2
            i.corners = i.corners.dot(b)
            i.corners[:, 0] = i.corners[:, 0] + self.width*0.9/2
            #i.corners[:, 2] = i.corners[:, 2] - self.depth/2

        self.calc_draw_points(self.scaled_draw_object)

    def z_spin_drawing(self, degree):
        self.canvas.fill(qc.Qt.black)
        degree = degree/720
        b_list = [[np.cos(degree), -np.sin(degree), 0], [np.sin(degree), np.cos(degree), 0], [0, 0, 1]]
        b = np.array(b_list)
        for i in self.scaled_draw_object.polygon_list:
            i.corners[:, 0] = i.corners[:, 0] - self.width*0.9/2
            i.corners[:, 1] = i.corners[:, 1] - self.height*0.9/2
            i.corners = i.corners.dot(b)
            i.corners[:, 0] = i.corners[:, 0] + self.width*0.9/2
            i.corners[:, 1] = i.corners[:, 1] + self.height*0.9/2

        self.calc_draw_points(self.scaled_draw_object)

    def move_x_direction(self, distance):
        self.canvas.fill(qc.Qt.black)
        for i in self.scaled_draw_object.polygon_list:
            i.corners[:, 0] = i.corners[:, 0] + distance
        self.calc_draw_points(self.scaled_draw_object)
        return



if __name__ == "__main__":
    """
    flache1 = Polygon([[100, 100, 200], [200, 100, 200], [200, 200, 200], [100, 200, 200]])
    flache2 = Polygon([[100, 100, 100], [200, 100, 100], [200, 200, 100], [100, 200, 100]])
    flache3 = Polygon([[100, 100, 200], [100, 100, 100], [100, 200, 100], [100, 200, 200]])
    flache4 = Polygon([[100, 100, 200], [200, 100, 200], [200, 100, 100], [100, 100, 100]])
    flache5 = Polygon([[200, 100, 200], [200, 100, 100], [200, 200, 100], [200, 200, 200]])
    flache6 = Polygon([[100, 200, 200], [100, 200, 100], [200, 200, 100], [200, 200, 200]])
    object1 = Object3D([flache1, flache2, flache3, flache4, flache5, flache6])
    projection1 = Projections(object1)
    """

    from test import get_bunny_data

    pts, face = get_bunny_data()

    areas = []
    for indices in face:
        polypoints = []
        for indice in indices:
            polypoints.append(list(pts[indice]))
            #print(polypoints)
        areas.append(Polygon(polypoints))

    object1 = Object3D(areas)
    app = qw.QApplication(sys.argv)
    #w = Window(object1)
    w = ObjectWidget(object1)
    w1 = Window(w)
    app.exec_()