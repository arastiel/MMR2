import tarfile
import os
from os.path import join
from plyfile import PlyData
import numpy as np

def get_bunny_data():
    bunny_tar_file = tarfile.open('bunny.tar.gz')
    try:
        os.mkdir('bunny_data')
    except:
        pass
    bunny_tar_file.extractall('bunny_data')
    bunny_tar_file.close()

    # Path to the bunny ply file
    bunny_ply_file = join('bunny_data', 'bunny', 'reconstruction', 'bun_zipper_res4.ply')

    plydata = PlyData.read(bunny_ply_file)
    #print(plydata)
    vertex_data = plydata['vertex'].data # numpy array with fields ['x', 'y', 'z']
    pts = np.zeros([vertex_data.size, 3])
    pts[:, 0] = vertex_data['x']
    pts[:, 1] = vertex_data['y']
    pts[:, 2] = vertex_data['z']
    face_data = plydata['face'].data


    face = [list(row[0]) for row in face_data]

    return pts, face