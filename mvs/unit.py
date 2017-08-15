'''MVS Module Control System'''
import requests
from ipdb import set_trace as debug
import subprocess
import atexit
from hardware import Hardware

# Define base camera port number.
BASE_PORT = 1493


class Unit(object):

    def __init__(self, unit_id=0):

        # Handle camera configuration.
        self.unit_id = unit_id
        self.camera_port = BASE_PORT + unit_id
        self.video_url = 'http://localhost:{}/video_feed'.format(self.\
                camera_port)
        self.image_url = 'http://localhost:{}/current_image'.format(self.\
                camera_port)
        self.binary_image_url = 'http://localhost:{}/current_binary_image'.\
                format(self.camera_port)

        # Launch camera image server.
        self.boot_image_server()

        # Register motor controls.
        # TODO
        self.x = 0
        self.y = 0
        self.z = 0
        self.dx = 1
        self.dy = 1
        self.dz = 1

        # Create the Hardware.
        self.hardware = Hardware()

        # Clean up on exit.
        atexit.register(self.close)

    def boot_image_server(self):
        '''Launch the image server associated with the module.'''
        cmds = ['python', 'image_server.py', '--port', str(self.camera_port),\
                '--camera', str(self.unit_id)]
        self.image_server = subprocess.Popen(cmds)

    def close(self):
        '''Close down image server.'''
        print('Closing down image server.')
        self.image_server.kill()

    def take_picture(self):
        '''Take picture at current target position.'''
        response = requests.get(self.image_url)
        return response.content

    def move_to_target(self, position):
        '''Move module's camera to specified target.'''
        # Platform takes input as a list.
        target = [
            position['x'],
            position['y'],
            position['z']
        ]
        # Move
        self.hardware.generate_trajectory(target)

    @property
    def location(self):
        '''Return current location of hardware.'''
        return hardware.location


if __name__=='__main__':
    unit = Unit()
