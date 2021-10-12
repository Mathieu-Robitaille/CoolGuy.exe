import cv2
import imageio
import os
import pyfakewebcam
import validators
import numpy as np
import urllib.request
import effects
import time

from flask import Flask, request
from itertools import cycle
from threading import Thread

import tensorflow as tf
from tf_bodypix.model import DEFAULT_RESIZE_METHOD
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths


class BodyPix:
    # BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16 # Not omega mode : 0.030881166458129883
    # BodyPixModelPaths.RESNET50_FLOAT_STRIDE_16 # Omega mode : 2 powerful
    def __init__(
        self, 
        model: BodyPixModelPaths = BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16,
        resize_method: str = DEFAULT_RESIZE_METHOD
        ):
        # load model (once)
        self.bodypix_model = load_model(download_model(model))
        self.resize_method = resize_method
    
    def get_mask(self, capture) -> np.array:
        result = self.bodypix_model.predict_single(capture)
        return result.get_mask(threshold=0.75)


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

class Image_Handler:
    def __init__(
            self,
            width: int = 1280, 
            height: int = 720,
            flask_app: Flask = None, # This is probably pretty bad
            background_root_path: str = '/data/backgrounds',
            background_path: str = 'rat.gif',
            effect: effects.available_effects = effects.available_effects.no_effect
            ) -> None:
        self.width = width
        self.height = height
        
        self.background_root_path = background_root_path
        self.background_path = background_path

        self.background = None

        self.effect = effect

        self.flask_app = flask_app
        self.flask_app.add_url_rule('/', 'change_on_request',methods=["POST"])

    def change_effect(self, new_effect: effects.available_effects) -> None:
        self.effect = new_effect

    def apply_effect(self, frame):
        if self.effect == effects.available_effects.no_effect:
            pass
        return effects.apply_effect(frame, self.effect)

    def composite_frames(self, capture: np.array, mask: np.array) -> np.array:
        inv_mask = 1 - mask
        bg = next(self.background)
        # Have fun :)
        for c in range(capture.shape[2]):
            capture[:, :, c] = capture[:, :, c] * mask[:, :, 0] + \
                bg[:, :, c] * inv_mask[:, :, 0]
        return capture

    def load_gif(self, uri):
        gif = imageio.mimread(uri)
        conv_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif]
        scaled_gif = np.array([cv2.resize(frame, (self.width, self.height)) for frame in conv_gif])
        self.background = cycle(scaled_gif)

    def load_image(self, uri):
        img = cv2.imread(uri)
        scaled_img = cv2.resize(img, (self.width, self.height))
        self.background = cycle([scaled_img])

    def load_background(self, uri):
        ext = os.path.splitext(uri)[-1]
        if ext == ".gif":
            print("loading Gif")
            self.load_gif(uri)
        if ext == ".jpg":
            print("loading jpg")
            self.load_image(uri)

    def change_background(self, filename):
        path = f"{self.background_root_path}/{filename}"
        print(f"Loading {path}")
        # This should just accept an array?
        if not os.path.exists(path):
            print("Path does not exist")
            raise FileNotFoundError
        self.background_path = filename
        self.load_background(path)
    
    def download_object(self, url, filename):
        if os.path.exists(f"{self.background_root_path}/{filename}"):
            return True
        try:
            data = bytearray(urllib.request.urlopen(url).read())
            with open(f"{self.background_root_path}/{filename}", "wb+") as file_handler:
                file_handler.write(data)
        except Exception as e:
            print(e)
            return False
        return True

    # Whoooooooo boy this is poop
    def change_on_request(self):
        try:
            req = request.get_json()
            download_status = True
            if 'url' in req and 'filename' in req:
                if validators.url(req['url']):
                    download_status = self.download_object(req['url'], req['filename'])
            if 'filename' in req and download_status:
                self.change_background(req['filename'])
        except Exception as e:
            print(e)
            return "There was a fucky wucky\n"
        return "Yay!\n"


def main():
    # Init Flask
    app = Flask(__name__)
    kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}
    
    bodypix = BodyPix()
    camera = Camera()
    ih = Image_Handler(flask_app=app)

    # Set up background
    ih.change_background(ih.background_path)

    flaskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()

    print("Starting camera app")

    # frames forever
    while True:
        start_time = time.time()
        try:
            frame_start_time = time.time()
            frame = camera.get_frame()
            print(f'Time to get the frame: {time.time() - frame_start_time}')

            mask_start_time = time.time()
            mask = bodypix.get_mask(capture=frame)
            print(f'Time to get the mask: {time.time() - mask_start_time}')

            effect_start_time = time.time()
            frame = ih.apply_effect(frame)
            print(f'Time to apply effects: {time.time() - effect_start_time}')

            composite_start_time = time.time()
            composited_frame = ih.composite_frames(capture=frame, mask=mask)
            print(f'Time to composite the frame: {time.time() - composite_start_time}')

            schedule_start_time = time.time()
            camera.schedule_frame(composited_frame)
            print(f'Time to schedule the frame:  {time.time() - schedule_start_time}')
        except Exception as e:
            print(e)
        print(f'Execution for this loop took {time.time() - start_time}')


if __name__ == "__main__":
    main()

