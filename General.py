import numpy as np
import numpy.ma as ma

def rotation_matrix_z_axis(theta):
    return ma.masked_inside(np.array([[np.cos(theta), -np.sin(theta), 0.],[np.sin(theta), np.cos(theta), 0.],[0., 0., 1.]]),-10 ** (-15),10 ** (-15)).filled(0.)

def rotation_matrix_y_axis(phi):
    return ma.masked_inside(np.array([[np.cos(phi), 0., np.sin(phi)],[0., 1., 0.],[-np.sin(phi), 0., np.cos(phi)]]),-10 ** (-15),10 ** (-15)).filled(0.)