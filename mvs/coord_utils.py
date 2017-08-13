import numpy as np


class Position(object):

    def __init__(self, x, y, z):
        '''Initialize with rectangular coordinates.'''
        self.x = x
        self.y = y
        self.z = z

    @property
    def r(self):
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def cylindrical(self):
        '''Return current cylindrical coordinates.'''
        return np.array([self.r, self.theta, self.z])

    @property
    def rect(self):
        return np.array([self.x, self.y, self.z])

    @property
    def theta(self):
        '''Current angle in polar coordinate system.'''
        return np.arctan2(self.y, self.x)

    @property
    def C(self):
        '''Computes the transformation matrix between polar and rect deltas.'''
        return np.array([[np.cos(self.theta), -self.r * np.sin(self.theta)],\
                [np.sin(self.theta), self.r * np.cos(self.theta)]])

    def drect_to_dpolar(self, dx=0, dy=0, dz=0):
        '''Convert delta in rectangular coordinates to polar delta.'''
        v = np.array([dx, dy])
        return np.hstack((np.linalg.inv(self.C).dot(v), dz))

