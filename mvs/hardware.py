from motor import Motor
from cord_utility import Position
import numpy as np
from ipdb import set_trace as db
from math import atan2


# Define the number of steps for the motor
# to complete a single full rotation.
FULL_CIRCLE = 510.0

# Number of millimeters per step for DR and DZ.
# Amount of radians per one step for DTHETA
MM_PER_STEP_DZ = 0.0062
RAD_PER_STEP_DT = 0.00147
MM_PER_STEP_DR = 0.123

# Inverse relations.
DZ_TO_MM_PER_STEP = 1 / MM_PER_STEP_DZ
DT_TO_RAD_PER_STEP = 1 / RAD_PER_STEP_DT
DR_TO_MM_PER_STEP = 1 / MM_PER_STEP_DR

# Default number of steps for movement.
N_STEPS = 10


class Hardware(object):
    # Models the physical platform of the device.
    # Controls the three onboard motors.

    def __init__(self, r_int = 0, t_int = 0, z_int = 0):
        # Begins at the origin [0, 0, 0]
        self.motor = Motor()
        self.position = Position()
        self.trajectory = []
        self.__dict__['target'] = []
        self.plot = []
        self.r_steps = r_int
        self.theta_steps = t_int
        self.z_steps = z_int

        # If there were provided coordinates, start there.
        if r_int + t_int + z_int > 0:
            self.begin()

    def __setattr__(self, name, value):
        if name == 'target':
            self.__dict__[name] = value
            self.generate_trajectory(value)

        else:
            self.__dict__[name] = value

    def begin(self):
        # Start the platform at a given step location.
        self.plot = self.motor.move([self.r_steps, self.theta_steps, self.z_steps])

        delta = [
            self.r_steps * MM_PER_STEP_DR,
            self.theta_steps * RAD_PER_STEP_DT,
            self.z_steps * MM_PER_STEP_DZ
        ]
        # Update the platform position.
        self.position.update(delta)

    def generate_trajectory(self, target):
        # Generate a list of steps required to move to a target.
        current = self.position.rect
        if self.check_rotation(current, target):

            polar_target = [
                np.sqrt(target[0] ** 2 + target[1] ** 2),
                atan2(target[1], target[0]),
                target[2]
            ]

            delta = [
                polar_target[0] - self.position.r,
                polar_target[1] - self.position.theta,
                polar_target[2] - self.position.z
            ]

            r_steps = np.round(delta[0] * DR_TO_MM_PER_STEP)
            theta_steps = np.round(delta[1] * DT_TO_RAD_PER_STEP)
            z_steps = np.round(delta[2] * DZ_TO_MM_PER_STEP)

            self.r_steps += r_steps
            self.theta_steps += theta_steps
            self.z_steps += z_steps

            self.plot = self.motor.move([r_steps, theta_steps, z_steps])

            # # Delta S is fixed at 1mm resolution.
            # DELTA_S = 1
            #
            # # Empty the trajectory list.
            # self.trajectory = []
            #
            # # Create another position object to keep track of where we are in
            # # the trajectory list.
            # self.current = Position(x = self.position.x, y = self.position.y, \
            #                                                     z = self.position.z)
            #
            # keep_moving = True
            # self.plot.append(self.current.rect)

            # while keep_moving:
            #     # Calculate the new cartesian deltas.
            #     # rect = self.rect_delta(target, DELTA_S, self.current.rect)
            #
            #     cyl_delta = self.cyl_delta(polar_target, self.current.cylindrical)
            #
            #     # Get the cylindrical delta measurements.
            #     # polar = self.position.drect_to_dpolar(rect[0], rect[1], rect[2])
            #
            #     # Find the ratio between DT and DR.
            #     ratio = cyl_delta[1] / cyl_delta[0]
            #
            #     # Get a list of the max steps to take.
            #     max_steps = self.get_steps(cyl_delta, ratio)
            #
            #     # Determine the direction of the movement.
            #     r_steps = max_steps[0] * np.sign(cyl_delta[0])
            #     theta_steps = max_steps[1] * np.sign(cyl_delta[1])
            #     print("max steps:" + str(max_steps[1]))
            #     print("sign: " + str(np.sign(cyl_delta[1])))
            #     z_steps = max_steps[2] * np.sign(cyl_delta[2])
            #
            #     # Make a list of the steps required to reach a target.
            #     self.trajectory.append([r_steps, theta_steps, z_steps])
            #
            #     # Update the coordinate systems.
            #     real_delta = [
            #         r_steps * MM_PER_STEP_DR,
            #         theta_steps * RAD_PER_STEP_DT,
            #         z_steps * MM_PER_STEP_DZ
            #     ]
            #     self.current.update(real_delta)
            #     self.plot.append(self.current.rect)
            #
            #     keep_moving = r_steps + theta_steps + z_steps > 0



    def rect_delta(self, target, DELTA_S, position):
        # Compute the remaining cartesian distances.
        delta_x = target[0] - position[0]
        delta_y = target[1] - position[1]
        delta_z = target[2] - position[2]

        # Calculate the local deltas.
        x_diff = (delta_x * DELTA_S) / np.sqrt(delta_x ** 2 + delta_y ** 2)
        y_diff = (delta_y * DELTA_S) / np.sqrt(delta_x ** 2 + delta_y ** 2)

        # Return the local deltas. Local  DZ will be determined later by the steps measurement.
        return [x_diff, y_diff, delta_z]


    def get_steps(self, cyl_delta, ratio):
        # Find the amount of steps to take this iteration.
        # If we are closer than N steps, choose that.
        max_r_steps = min(N_STEPS, np.round(cyl_delta[0] * DR_TO_MM_PER_STEP))

        max_theta_steps = min(np.round(N_STEPS * ratio), np.round(cyl_delta[1] * DT_TO_RAD_PER_STEP))

        max_z_steps = min(N_STEPS, np.round(cyl_delta[2] * DZ_TO_MM_PER_STEP))

        return [max_r_steps, max_theta_steps, max_z_steps]


    def move_to(self, cords):
        # Move to a location!
        # Generate cartesian deltas.
        current = self.position.cartesian
        cart_delta = [
            cords[0] - current[0],
            cords[1] - current[1],
            cords[2] - current[2]
        ]

        # Move!
        self.move(cart_delta)


    def check_rotation(self, current, target):
        # Check to see if the motors will cross the boundary
        # at pi.  If they will, redirect!

        # m = (y2 - y1) / (x2 - x1)
        slope = (target[1] - current[1]) / (target[0] - current[0])
        # b = y - mx
        y_intercept = current[1] - (slope * current[0])
        # x_int = b / m
        x_intercept = y_intercept / slope

        if  x_intercept < 0:
            # Abort!  We can't cross the boundary between
            # quadrants II and III due to local mechanics.
            # Go to the (0, 0, 0) position (reset theta as well),
            # and continue from there.
            self.generate_trajectory(0, 0, current[2])
            self.generate_trajectory(target)
            return False

        return True


    def move(self):
        # Tell the motors to move with the last generated trajectory.
        self.motor.move(self.trajectory)


    @property
    def location(self):
        return self.position.cartesian


    @property
    def step_location(self):
        return [self.r_steps, self.theta_steps, self.z_steps]





# --------------------------- TEST -----------------------------------------



if __name__ == '__main__':

    import pylab as plt
    plt.ion()

    plat = Hardware()

    line = []

    plat.target = [0, 0.5, 0]
    r = plat.plot[0]
    t = plat.plot[1]

    #plat.target = [-1, -1, 0]

    #line += plat.plot

    for i in range(len(t) - len(r)):
        r.append(r[-1])

    xy = [[rr * np.cos(tt), rr*np.sin(tt)] for rr,tt in zip(r,t)]

    xy = np.array(xy)

    plt.plot(xy[:,0], xy[:,1])




# -----------------------------------------------------------------------------
