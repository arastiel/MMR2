from geometry import Vector, Sphere, Line, Plane, Triangle
from intersection import intersection
import numpy as np
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class RaytracerView(qw.QMainWindow):
    def __init__(self):
        qw.QMainWindow.__init__(self)

        # init
        self.init_window()
        self.init_canvas()

        self.background_color = qc.Qt.yellow
        self.camera = Vector(0, 0, -1)

        self.create_objects()
        self.raytrace()
        self.show_canvas()
        self.show()

    def init_window(self):
        self.setWindowTitle("Raytracing")
        self.height = 300
        self.width = 300
        self.setFixedSize(self.width, self.height)

    def init_canvas(self):
        # Label to display objects
        self.display = qw.QLabel()
        self.setCentralWidget(self.display)

        # canvas on which we paint
        self.canvas = qg.QPixmap(self.width, self.height)
        self.painter = qg.QPainter(self.canvas)
        self.painter.fillRect(0, 0, self.width, self.height, qc.Qt.white)
        self.painter.end()

        # Scene on which we will manipulate pixels
        self.scene = np.zeros([self.height, self.width, 4], dtype=np.uint8)

    def show_canvas(self):
        # convert our scene to an Image after raytracing
        self.scene = qg.QImage(self.scene.data, self.width, self.height, qg.QImage.Format_RGBA8888)

        # draw scene on canvas
        self.painter = qg.QPainter(self.canvas)
        self.painter.drawImage(0, 0, self.scene)

        # show
        self.display.setPixmap(self.canvas)

    def create_objects(self):
        # e1 = Plane()

        #(+x nach rechts, -x nach links)(+y nach unten, -y nach oben)(+z nach hinten, -z nach vorne)

        #light setting 1 / links oben (gleiche ebene wie objekte)
        #self.light = Vector(-1, -1, -1)

        #light setting 2 / von rechts über die objekte
        self.light = Vector(1, 1, -2)

        #cube points
        a = Vector(-1.25, .5, 1.)
        b = Vector(-.75, .5, 1.)
        c = Vector(-.75, 1., 1.)
        d = Vector(-1.25, 1., 1.)
        e = Vector(-1.25, .5, 2)
        f = Vector(-.75, .5, 2)
        g = Vector(-.75, 1., 2)
        h = Vector(-1.25, 1., 2)

        #triangle of cubes
        abd = Triangle(a, b, d)
        bdc = Triangle(b, d, c)
        aeb = Triangle(a, e, b)
        bef = Triangle(b, e, f)
        bcf = Triangle(b, c, f)
        fcg = Triangle(f, c, g)
        aed = Triangle(a, e, d)
        edh = Triangle(e, d, h)
        cdh = Triangle(c, d, h)
        cgh = Triangle(c, g, h)
        hef = Triangle(h, e, f)
        fgh = Triangle(f, g, h)

        #(+x nach rechts, -x nach links)(+y nach unten, -y nach oben)(+z nach hinten, -z nach vorne)

        s = Sphere(center=Vector(0, -1, 2), r=.75)
        #t1 = Triangle(Vector(-4, 1.75, 2.), Vector(0, -2.5, 2), Vector(6., 1.75, 2.))
        #t2 = Triangle(Vector(-4., 1.75, 2.), Vector(0, 2.5, 2), Vector(6., 1.75, 2.))

        t3 = Triangle(Vector(0, 0, 2), Vector(0, -4, 2), Vector(-4, 0, 2))
        t4 = Triangle(Vector(0, 0, 2), Vector(0, 4, 2), Vector(-4, 0, 2))
        t5 = Triangle(Vector(0, 0, 2), Vector(0, -4, 2), Vector(4, 0, 2))
        t6 = Triangle(Vector(0, 0, 2), Vector(0, 4, 2), Vector(4, 0, 2))


        cube = [abd, bdc, aeb, bef, bcf, fcg, aed, edh, cdh, cgh, hef, fgh]
        for cube_part in cube:
            cube_part.color = np.array([25, 66, 234, 255])

        self.objects = [t3, t4, t5, t6, s] + cube

    def raytrace(self):
        r = self.width / self.height
        px = np.linspace(-1, 1, self.width)
        py = np.linspace(-1 / r, 1 / r, self.height)

        for i, x in enumerate(px):
            if i % 10 == 0:
                print(i / self.width * 100, "%")
            for j, y in enumerate(py):
                hitlist = []    # store every intersection

                for obj in self.objects:
                    # Primärstrahl = Gerade von Kamera zum Object durch den Bildschirm (P = (x, y, 0))
                    target = Vector(x, y, 0)
                    d = target - self.camera
                    d_norm = d.normalize()
                    pr_ray = Line(self.camera, d_norm)

                    # append each intersection found to hitlist (object, distance, SP)
                    intersect = intersection(pr_ray, obj)
                    if intersect:
                        hitlist.append((obj, intersect[1], intersect[0]))

                if not hitlist:
                    # if no object hit - color it in outer space (background color)
                    self.scene[j][i] = [56, 56, 56, 255]

                else:
                    #get the nearest object and calculate the lightning
                    nearest = min(hitlist, key=lambda x: x[1])

                    #get norm_vector for lightning (sphere needs SP)
                    if isinstance(nearest[0], Sphere):
                        norm_vec = (nearest[0].get_norm_vec(nearest[2])).normalize()
                    else:
                        norm_vec = nearest[0].get_norm_vec()

                    winkel = np.cos(norm_vec * self.light/(abs(norm_vec)*abs(self.light)))
                    new = np.copy(nearest[0].color)
                    #calc new saturation
                    new[3] = new[3] * winkel
                    

                    #secondary ray for shadowing
                    sec_ray = Line(nearest[2], (self.light - nearest[2]))
                    shadowed = False

                    #check if that secondary ray intersects with any object if yes, paint it black
                    for obj in self.objects:
                        if obj == nearest[0]:   #skip objects of the used intersection point
                            continue
                        intersect = intersection(sec_ray, obj)
                        if intersect:
                            if intersect[1] < nearest[1]:  # check if intersection of secondary ray
                                shadowed = True            # is smaller than nearest object in that pixel
                                break
                    if shadowed:
                        self.scene[j][i] = [0, 0, 0, 255]  # if yes, paint it black
                    else:
                        self.scene[j][i] = new             # else paint it with calculated saturation


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    View = RaytracerView()
    sys.exit(app.exec_())
