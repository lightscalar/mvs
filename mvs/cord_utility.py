import numpy as np
from ipdb import set_trace as db
from math import cos, sin

class Position(object):


    def __init__(self, x = 0, y = 0, z = 0):
        '''Initialize with rectangular coordinates.'''
        self.__dict__['x'] = x
        self.__dict__['y'] = y
        self.__dict__['z'] = z
        self.__dict__['theta'] = 0
        self.__dict__['r'] = 0

        # Ensure that coordinates are all set.
        self.x = self.x
        self.y = self.y


    def __setattr__(self, name, value):
        # Update the opposite coordinate system when
        # a value is manually updated.
        self.__dict__[name] = value

        if name == 'x' or name == 'y':
            self.__dict__['r'] = np.sqrt(self.x**2 + self.y**2)
            self.__dict__['theta'] = np.arctan2(self.y, self.x)

        elif name == 'r' or name == 'theta':
            self.__dict__['x'] = self.r * cos(self.theta)
            self.__dict__['y'] = self.r * sin(self.theta)


    def update(self, polar_deltas):
        # Update the current coordinates.
        self.r += polar_deltas[0]
        self.theta += polar_deltas[1]
        self.z += polar_deltas[2]


    @property
    def cylindrical(self):
        '''Return current cylindrical coordinates.'''
        return np.array([self.r, self.theta, self.z])


    @property
    def rect(self):
        return np.array([self.x, self.y, self.z])


    @property
    def C(self):
        '''Computes the transformation matrix between polar and rect deltas.'''
        return np.array([[np.cos(self.theta), -self.r * np.sin(self.theta)],\
                [np.sin(self.theta), self.r * np.cos(self.theta)]])


    def drect_to_dpolar(self, dx=0, dy=0, dz=0):
        '''Convert delta in rectangular coordinates to polar delta.'''
        v = np.array([dx, dy])
        if self.r == 0:
            return [np.sqrt(dx**2 + dy**2), 0, dz]

        return np.hstack((np.linalg.inv(self.C).dot(v), dz))





# -----------------------------------------------------------------------------
