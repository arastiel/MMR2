import numpy as np

class Polygon:
    def __init__(self, corners):
        self.corners = np.array(corners)
        self.rgb = list(np.random.choice(range(256), size=3))
        #print("NOW")
        #print(self.get_max_x())

    def get_min_x(self):
        return np.amin(self.corners, axis=0)[0]

    def get_max_x(self):
        return np.amax(self.corners, axis=0)[0]

    def get_min_y(self):
        return np.amin(self.corners, axis=0)[1]

    def get_max_y(self):
        return np.amax(self.corners, axis=0)[1]

    def get_min_z(self):
        return np.amin(self.corners, axis=0)[2]

    def get_max_z(self):
        return np.amax(self.corners, axis=0)[2]


class Object3D:
    def __init__(self, polygon_list):
        self.polygon_list = np.array(polygon_list)
        #print(self.polygon_list[0].corners)

    def get_min_x(self):
        mins_x = [mins.get_min_x() for mins in self.polygon_list]
        return np.min(mins_x)

    def get_max_x(self):
        maxs_x = [maxs.get_max_x() for maxs in self.polygon_list]
        return np.max(maxs_x)

    def get_min_y(self):
        mins_y = [mins.get_min_y() for mins in self.polygon_list]
        return np.min(mins_y)

    def get_max_y(self):
        maxs_y = [maxs.get_max_y() for maxs in self.polygon_list]
        return np.max(maxs_y)

    def get_min_z(self):
        mins_z = [mins.get_min_z() for mins in self.polygon_list]
        return np.max(mins_z)

    def get_max_z(self):
        maxs_z = [maxs.get_max_z() for maxs in self.polygon_list]
        return np.max(maxs_z)