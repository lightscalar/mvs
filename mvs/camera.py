import cv2
import time
from imutils.video import VideoStream

class Camera(object):
    '''Connect to specified camera; take pictures.'''

    def __init__(self, src = 0):
        # Initialize as a VideoCapture object.
        self.stream = cv2.VideoCapture(src)
        # Warm the camera up.
        time.sleep(1)
        # Ramp the camera and adjust to light levels.
        for i in range(15):
            _, frame = self.stream.read()

    def get_image(self):
        # Read an image and return it as a jpeg.
        _, frame = self.stream.read()
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()

    def get_jpeg(self):
        # Read an image and return a 2D array.
        _, frame = self.stream.read()
        return frame

    def __del__(self):
        # Clean up.
        del(self.stream)
