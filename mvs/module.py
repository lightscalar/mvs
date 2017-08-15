'''MVS Module Control System'''
import requests
from ipdb import set_trace as debug
import subprocess
import atexit
from platform import Platform

# Define base camera port number.
BASE_PORT = 1493


class Module(object):


    def __init__(self, module_id=0):

        # Handle camera configuration.
        self.module_id = module_id
        self.camera_port = BASE_PORT + module_id
        self.video_url = 'http://localhost:{}/video_feed'.format(self.\
                camera_port)
        self.image_url = 'http://localhost:{}/current_image'.format(self.\
                camera_port)
        self.binary_image_url = 'http://localhost:{}/current_binary_image'.\
                format(self.camera_port)

        self.platform = Platform()

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

        # Clean up on exit.
        atexit.register(self.close)


    def boot_image_server(self):
        '''Launch the image server associated with the module.'''
        cmds = ['python', 'image_server.py', '--port', str(self.camera_port),\
                '--camera', str(self.module_id)]
        self.image_server = subprocess.Popen(cmds)


    def close(self):
        '''Close down image server.'''
        print('Closing down image server.')
        self.image_server.kill()


    def move_to_target(self, position):
        '''Move module's camera to specified target.'''
        # Platform takes input as a list.
        target = [
            position['x'],
            position['y'],
            position['z']
        ]
        # Move
        self.platform.generate_trajectory(target)


    def move(self, delta):
        '''Move up by increment dy.'''
        x = self.x + delta[0]
        y = self.y + delta[1]
        z = self.z + delta[2]
        self.move_to_target(x, y, z)


    def take_picture(self):
        '''Take picture at current target position.'''
        response = requests.get(self.image_url)
        return response.content


    @property
    def current_location(self):
        '''Returns tuple (x,y,z) corresponding to current cameras position.'''
        raise NotImplementedError


if __name__=='__main__':

    module = Module()
