import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import numpy as np
# from Aufgabe1 import Graph
from graph import Graph
from skimage.draw import line
from functools import partial
import itertools


class MyMainWindow(qw.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.setWindowTitle("Dijsktra")
        self.main_widget = qw.QWidget()
        self.main_widget.setContentsMargins(0, 0, 0, 0)

        self.height = 1000
        self.width = 800
        self.setFixedWidth(self.width)


        self.map_widget = MapWidget()

        self.main_layout = qw.QVBoxLayout()
        #self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.map_widget)

        self.button_widget = qw.QWidget()
        self.button1 = qw.QPushButton("Start Dijkstra")
        self.button1.clicked.connect(self.run_dijkstra)
        self.button1.setToolTip("Start Dijkstra with s = bluepoint and t = redpoint")
        self.button2 = qw.QPushButton("Reset")
        self.button2.setToolTip("Reset Map")
        self.button2.clicked.connect(self.map_widget.resetMap)

        self.button_layout = qw.QGridLayout()
        self.button_layout.addWidget(self.button1, 0, 0, 1, 1)
        self.button_layout.addWidget(self.button2, 0, 2, 1, 1)

        self.button_widget.setLayout(self.button_layout)
        self.main_layout.addWidget(self.button_widget)

        self.help_text_points = qw.QLabel("Blauer Punkt = Start, Roter Punkt = Ende")
        self.main_layout.addWidget(self.help_text_points)

        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.show()

    def run_dijkstra(self):
        start = int(self.get_widget_start()[0])
        end = int(self.get_widget_end()[0])

        if start and end:
            self.map_widget.paint_dijkstra(start, end)
            return 1

        return 0

    def get_widget_start(self):
        return self.map_widget.start

    def get_widget_end(self):
        return self.map_widget.end


class MapWidget(qw.QWidget):
    def __init__(self):
        super(MapWidget, self).__init__()
        self.graph = Graph("edges.csv", "nodes.csv")

        self.start = None
        self.end = None
        self.setContentsMargins(0, 0, 0, 0)
        # fenster
        self.height = 800
        self.width = 800
        self.setGeometry(0, 0, self.width, self.height)


        # einfaches lgs mit 2 funktionen und 2 variablen
        self.a_x = self.width / (self.graph.get_max_lg() - self.graph.get_min_lg())
        self.c_x = -(self.a_x * self.graph.get_min_lg())

        self.a_y = self.height / (self.graph.get_max_bg() - self.graph.get_min_bg())
        self.c_y = -(self.a_y * self.graph.get_min_bg())

        self.display = qw.QLabel()
        self.display.setContentsMargins(0, 0, 0, 0)

        # mousetracking on widget
        self.mousePressEvent = self.getTestNodes

        self.canvas = qg.QPixmap(self.width, self.height)
        self.painter = qg.QPainter(self.canvas)
        self.painter.fillRect(0, 0, self.width, self.height, qc.Qt.lightGray)

        self.city_map = np.zeros([self.height, self.width, 4], dtype=np.uint8)
        self.fill_map()

        self.city_map_img = qg.QImage(self.city_map.data, self.width, self.height, qg.QImage.Format_RGBA8888)

        self.painter.drawImage(0, 0, self.city_map_img)

        self.display.setPixmap(self.canvas)

        self.map = qw.QHBoxLayout()
        self.map.addWidget(self.display)
        self.map.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.map)

    def fill_map(self):
        # draw nodes
        for node in self.graph.nodes:
            # x berechnen für pixel
            lg = node[1][0]
            x = int(self.a_x * lg + self.c_x)
            # y berechnen
            bg = node[1][1]
            y = int(self.a_y * bg + self.c_y)
            self.city_map[y - 1][x - 1] = [0, 0, 0, 255]
        # draw edges
        for edge in self.graph.edges:
            # lg, bg of first node of edge
            lg1, bg1 = self.graph.nodes[self.graph.data[edge[0][0]]][1]
            # lg, bg of second node of edge
            lg2, bg2 = self.graph.nodes[self.graph.data[edge[0][1]]][1]
            # calculate x and y of first node
            x1 = int(self.a_x * lg1 + self.c_x)
            y1 = int(self.a_y * bg1 + self.c_y)
            # calculate x and y of second node
            x2 = int(self.a_x * lg2 + self.c_x)
            y2 = int(self.a_y * bg2 + self.c_y)
            # draw line between nodes
            rr, cc = line(y1 - 1, x1 - 1, y2 - 1, x2 - 1)
            self.city_map[rr, cc] = [0, 0, 0, 255]

    def getTestNodes(self, e):
        self.painter.end()
        if e.button() == qc.Qt.LeftButton:
            min_dist = np.inf
            min_node = 0
            min_m_x = 0
            min_m_y = 0
            for node in self.graph.nodes:
                m_x = (self.a_x * node[1][0] + self.c_x)
                m_y = (self.a_y * node[1][1] + self.c_y)
                curr_dist = np.sqrt((e.pos().x() - m_x) ** 2 + (e.pos().y() - m_y) ** 2)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    min_m_x = int(m_x)
                    min_m_y = int(m_y)
                    min_node = node

            if self.start and self.end:
                print("reset")
                self.resetMap()

            elif self.start is None:
                print("start")
                self.painter = qg.QPainter(self.canvas)
                self.painter.setPen(qg.QColor(0, 255, 255))
                self.painter.setBrush(qg.QBrush(qg.QColor(0, 255, 255)))
                self.start = min_node

            elif self.end is None:
                print("end")
                self.painter = qg.QPainter(self.canvas)
                self.painter.setPen(qg.QColor(255, 0, 0))
                self.painter.setBrush(qg.QBrush(qg.QColor(255, 0, 0)))
                self.end = min_node

            self.painter.drawEllipse(min_m_x - 1, min_m_y - 1, 5, 5)
            self.painter.end()
            self.display.setPixmap(self.canvas)

    def resetMap(self):
        self.start = None
        self.end = None

        self.painter = qg.QPainter(self.canvas)
        self.painter.fillRect(0, 0, self.width, self.height, qc.Qt.lightGray)

        self.city_map = np.zeros([self.height, self.width, 4], dtype=np.uint8)
        self.fill_map()

        self.city_map_img = qg.QImage(self.city_map.data, self.width, self.height, qg.QImage.Format_RGBA8888)

        self.painter.drawImage(0, 0, self.city_map_img)

        self.display.setPixmap(self.canvas)
        self.painter.end()

    def paint_dijkstra(self, start, end):
        self.painter.end()
        self.painter = qg.QPainter(self.canvas)
        self.painter.setPen(qg.QColor(255, 255, 0))
        self.painter.setBrush(qg.QBrush(qg.QColor(255, 255, 0)))
        edge_list = (self.graph.djikstra(start, end))

        if edge_list == ("Kein Weg gefunden"):
            return

        copy_city_map = self.city_map

        for edge in edge_list:
            lg1, bg1 = self.graph.nodes[self.graph.data[edge[0][0]]][1]
            # lg, bg of second node of edge
            lg2, bg2 = self.graph.nodes[self.graph.data[edge[0][1]]][1]
            # calculate x and y of first node
            x1 = int(self.a_x * lg1 + self.c_x)
            y1 = int(self.a_y * bg1 + self.c_y)
            # calculate x and y of second node
            x2 = int(self.a_x * lg2 + self.c_x)
            y2 = int(self.a_y * bg2 + self.c_y)
            # draw line between nodes
            rr, cc = line(y1 - 1, x1 - 1, y2 - 1, x2 - 1)
            copy_city_map[rr, cc] = [255, 255, 0, 255]

        dijkstra_img = qg.QImage(copy_city_map, self.width, self.height, qg.QImage.Format_RGBA8888)
        self.painter.drawImage(0, 0, dijkstra_img)
        self.display.setPixmap(self.canvas)
        self.painter.end()

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    map = MyMainWindow()
    sys.exit(app.exec_())
