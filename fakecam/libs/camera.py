import cv2
from numpy.core.fromnumeric import resize
import pyfakewebcam
from typing import Tuple

from libs import timer

class CameraCaptureError(Exception):
    print("We failed to capture a frame from the camera.")

class Camera:

    def __init__(
            self,
            video_device: str = '/dev/video0',
            camera_capture_size: Tuple = (640, 480),
            final_size: Tuple = (1280, 720)
            ):
        self.camera_capture_size = camera_capture_size
        self.final_size = final_size
        self.cap = cv2.VideoCapture(video_device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_capture_size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_capture_size[1])
        self.cap.set(cv2.CAP_PROP_FPS, 30)


        self.fakecam = pyfakewebcam.FakeWebcam('/dev/video20', self.final_size[0], self.final_size[1])

    @timer.time_func
    def get_frame(self):
        """Get a frame from the camera"""
        status, frame = self.cap.read()
        if not status:
            raise CameraCaptureError
        return frame
    
    @timer.time_func
    def schedule_frame(self, frame):
        """Send a frame to the virtual camera"""
        next_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.fakecam.schedule_frame(next_frame)
