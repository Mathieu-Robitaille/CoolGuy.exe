import cv2
import pyfakewebcam

class Camera:

    def __init__(
            self,
            video_device: str = '/dev/video0',
            width: int = 1280, 
            height: int = 720
            ):
        self.cap = cv2.VideoCapture(video_device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        self.width = width
        self.height = height

        self.fakecam = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

    def get_frame(self):
        _, frame = self.cap.read()
        return frame
    
    def schedule_frame(self, frame):
        next_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.fakecam.schedule_frame(next_frame)
