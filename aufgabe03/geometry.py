import numpy as np
#from intersection import intersection, intersection2, intersection3

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.coords = np.array([x, y, z], dtype=np.float64)
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return self.coords.__iter__()

    def __getitem__(self, index):
        return self.coords[index]

    def __str__(self):
        return str((self.coords[0], self.coords[1], self.coords[2]))

    # ----- overwrite add, sub, mul, abs ----- #

    def __add__(self, other):
        tmp = np.add(self.coords, other.coords)
        return Vector(tmp[0], tmp[1], tmp[2])

    def __sub__(self, other):
        tmp = np.subtract(self.coords, other.coords)
        return Vector(tmp[0], tmp[1], tmp[2])

    def __mul__(self, other):  
        if isinstance(other, int) or isinstance(other, float):  
            # mutliply with scalar (vector * scalar)
            tmp = np.multiply(self.coords, other)
            return Vector(tmp[0], tmp[1], tmp[2])
        elif isinstance(other, Vector):
            # scalar product (vector dot vector)
            return np.dot(self.coords, other.coords)
        else:
            # if other is not an int/float or Vector
            raise ValueError("ValueError exception thrown")

    def __abs__(self):
        # distance/length of vector (d = root(x^2 + y^2 + z^2) )  
        return np.sqrt(self.coords[0] ** 2 + self.coords[1] ** 2 + self.coords[2] ** 2)

    # ----- extra functions: cross product and normalization ----- #

    def cross_prod(self, other):
        # cross product  
        tmp = np.cross(self.coords, other.coords)
        return Vector(tmp[0], tmp[1], tmp[2])

    def normalize(self):
        #normalize vector
        length = abs(self)
        x, y, z = self.coords[0] / length, self.coords[1] / length, self.coords[2] / length
        return Vector(x, y, z)

    def get_length(self):
        return np.sqrt((self.x)**2 + (self.y)**2 + (self.z)**2)


class Line:
    # line 
    # containing: 1 sup vector + 1 direction vector
    def __init__(self, _sup, _dir):
        self.sup_vec = _sup
        self.dir_vec = _dir

    def get_point(self, r):
        # get the point of a line with factor r (g = sup_vec + r * dir_vec)
        return Vector((self.sup_vec[0] + r * self.dir_vec[0]),
                      (self.sup_vec[1] + r * self.dir_vec[1]),
                      (self.sup_vec[2] + r * self.dir_vec[2]))

    def __str__(self):
        return f"(x=%0.2f, y=%0.2f, z=%0.2f) + r * (x=%0.2f, y=%0.2f, z=%0.2f)" % (self.sup_vec[0],
            self.sup_vec[1], self.sup_vec[2], self.dir_vec[0], self.dir_vec[1], self.dir_vec[2])


class Plane:
    # plane
    # containing: 1 sup vector + 2 direction vectors
    def __init__(self, _sup, _dir1, _dir2):
        self.sup_vec = _sup
        self.dir_vec1 = _dir1
        self.dir_vec2 = _dir2
        self.color = np.array([88, 88, 88, 255])

    def get_point(self, s, t):
        # get the point of a line with factor r and s (E = sup_vec + s * dir_vec1 + t * dir_vec2)
        return Vector((self.sup_vec[0] + s * self.dir_vec1[0] + t * self.dir_vec2[0]),
                      (self.sup_vec[1] + s * self.dir_vec1[1] + t * self.dir_vec2[1]),
                      (self.sup_vec[2] + s * self.dir_vec1[2] + t * self.dir_vec2[2]))

    def get_norm_vec(self):
        return self.dir_vec1.cross_prod(self.dir_vec2)


    def __str__(self):
        return f"(x=%0.2f, y=%0.2f, z=%0.2f) + r * (x=%0.2f, y=%0.2f, z=%0.2f) + s * (x=%0.2f, y=%0.2f, z=%0.2f)" % (self.sup_vec[0],
            self.sup_vec[1], self.sup_vec[2], self.dir_vec1[0], self.dir_vec1[1], self.dir_vec1[2],
            self.dir_vec2[0], self.dir_vec2[1], self.dir_vec2[2])


class Sphere:
    # equation for a 3D sphere:
    # (x - x_c)^2 + (y - y_c)^2 + (z - z_c)^2 = r^2
    # where (x_c, y_c, z_c) is the center of the sphere

    def __init__(self, center=Vector(0,0,0), r=1):
        self.center = center
        self.r = r
        self.color = np.array([29, 70, 45, 255])

    def __str__(self):
        return f"(x - %0.2f)^2 + (y - %0.2f)^2 + (z - %0.2f)^2 = %0.2f^2" % (self.center[0],
            self.center[1], self.center[2], self.r)

    def get_norm_vec(self, sp):
        return (sp - self.center)


class Triangle:
    def __init__(self, a, b, c):
        self.sup_vec = a
        self.dir_vec1 = b-a
        self.dir_vec2 = c-a
        self.color = np.array([255, 70, 45, 255])

    def get_norm_vec(self):
        return self.dir_vec1.cross_prod(self.dir_vec2)