from geometry import Vector, Line, Sphere, Plane, Triangle
import numpy as np

def intersection(line, obj):
    # interstection line-plane
    if isinstance(obj, Plane):
        # line = plane / mit LGS r, s, t herausfinden
        a = np.array([[line.dir_vec.x, -obj.dir_vec1.x, -obj.dir_vec2.x],
                      [line.dir_vec.y, -obj.dir_vec1.y, -obj.dir_vec2.y],
                      [line.dir_vec.z, -obj.dir_vec1.z, -obj.dir_vec2.z]])

        b = np.array([obj.sup_vec.x - line.sup_vec.x,
                      obj.sup_vec.y - line.sup_vec.y,
                      obj.sup_vec.z - line.sup_vec.z])

        x = np.linalg.solve(a, b)
        # x[0] = r, x[1] = s, x[2] = t

        SP = line.get_point(x[0])
        dist = (line.sup_vec - SP).get_length()

        return SP, dist

    # intersection line-triangle
    if isinstance(obj, Triangle):
        #line = plane / mit LGS r, s, t herausfinden
        a = np.array([[line.dir_vec.x, -obj.dir_vec1.x, -obj.dir_vec2.x],
                     [line.dir_vec.y, -obj.dir_vec1.y, -obj.dir_vec2.y],
                     [line.dir_vec.z, -obj.dir_vec1.z, -obj.dir_vec2.z]])

        b = np.array([obj.sup_vec.x - line.sup_vec.x,
                      obj.sup_vec.y - line.sup_vec.y,
                      obj.sup_vec.z - line.sup_vec.z])

        x = np.linalg.solve(a, b)
        #x[0] = r, x[1] = s, x[2] = t

        #r > 0, s und t in R+, s+t <= 1, dann liegt SP im Dreieck
        if x[0] > 0 and x[1] >= 0 and x[2] >= 0 and x[1]+x[2] <= 1:

            SP = line.get_point(x[0])
            dist = (line.sup_vec - SP).get_length()
            #print(SP, dist)
            return SP, dist

        return False

    # intersection line-sphere
    if isinstance(obj, Sphere):
        a = line.sup_vec.x - obj.center.x
        b = line.sup_vec.y - obj.center.y
        c = line.sup_vec.z - obj.center.z

        # coeff1 = x_2**2 + y_2**2 + z_2**2
        coeff1 = line.dir_vec.x ** 2 + line.dir_vec.y ** 2 + line.dir_vec.z ** 2

        # coeff2 = 2*a*x_2 + 2*b*y_2 + 2*c*z_2
        coeff2 = 2 * a * line.dir_vec.x + 2 * b * line.dir_vec.y + 2 * c * line.dir_vec.z

        # coeff3 = a**2 + b**2 + c**2 - radius**2
        coeff3 = a ** 2 + b ** 2 + c ** 2 - obj.r ** 2
        coeff = [coeff1, coeff2, coeff3]

        # test ob imaginäre zahl
        disk = (coeff2) ** 2 - 4 * coeff1 * coeff3
        if disk < 0:
            return False

        r = np.roots(coeff)
        check = [res for res in r if res > 0]   #test ob r > 0
        if not check:
            return False
        r_min = min(check)

        SP = line.get_point(r_min)
        dist = (line.sup_vec - SP).get_length()
        return SP, dist

    return False