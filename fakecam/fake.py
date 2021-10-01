import cv2
import imageio
import numpy as np
import os
import pyfakewebcam
import requests
import urllib.request
import validators

from flask import Flask, request
from itertools import cycle
from threading import Thread
from time import sleep

root_path = "/home/jm/git/fake-camera/fakecam/backgrounds"
background_filename = "rat.gif"
height, width = 720, 1280


def get_mask(frame, bodypix_url='http://127.0.0.1:9000'):
    _, data = cv2.imencode(".jpg", frame)
    r = requests.post(
        url=bodypix_url,
        data=data.tobytes(),
        headers={'Content-Type': 'application/octet-stream'})
    mask = np.frombuffer(r.content, dtype=np.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))
    return mask


def get_frame(cap, background_scaled):
    _, frame = cap.read()
    # fetch the mask with retries (the app needs to warmup and we're lazy)
    # P O G F R O G S A Y S W A I T F O R I T
    mask = None
    while mask is None:
        try:
            mask = get_mask(frame)
        except requests.RequestException as e:
            print("Mask request failed, retrying")
            print(e)
            sleep(1)

    # composite the foreground and background
    inv_mask = 1 - mask
    for c in range(frame.shape[2]):
        frame[:, :, c] = frame[:, :, c] * mask + \
            background_scaled[:, :, c] * inv_mask
    return frame


def resize_image_array(gif, imwidth, imheight):
    conv_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif]
    scaled_gif = [cv2.resize(frame, (imwidth, imheight)) for frame in conv_gif]
    return scaled_gif


def resize_image(image, imwidth, imheight):
    return cv2.resize(image, (imwidth, imheight))


def load_gif(uri, imwidth, imheight):
    gif = imageio.mimread(uri)
    return resize_image_array(gif, imwidth, imheight)


def load_image(uri, imwidth, imheight):
    img = cv2.imread(uri)
    scaled_img = cv2.resize(img, (imwidth, imheight))
    # Put in a list so we can convert to a cycle and iterate over the same thing, it save us work later
    return [scaled_img]


def load_background(uri, imwidth, imheight):
    ext = os.path.splitext(uri)[-1]
    if ext == ".gif":
        return load_gif(uri, imwidth, imheight)
    if ext == ".jpg":
        return load_image(uri, imwidth, imheight)
    return None


def update_background_filename(filename):
    global background_filename
    background_filename = f"{filename}"


def change_background(filename):
    if not os.path.exists(f'{root_path}/{filename}'):
        return "Doesnt exist"
    update_background_filename(filename)
    return cycle(load_background(f"{root_path}/{filename}", imwidth=width, imheight=height))


def download_object(url, filename):
    if os.path.exists(f"{root_path}/{filename}"):
        return "File already exists"
    try:
        data = bytearray(urllib.request.urlopen(url).read())
        open(f"{root_path}/{filename}", "wb+").write(data)
    except Exception as e:
        print(e)
        return "There was an error, check the logs"
    return "Success"


#####
# FLASK - Yes i know this is bad, fuck off
# Flask setup
app = Flask(__name__)


@app.route("/", methods=["POST"])
def change_on_request():
    try:
        req = request.get_json()
        if 'url' in req and 'filename' in req:
            if validators.url(req['url']):
                download_object(req['url'], req['filename'])
        if 'filename' in req:
            update_background_filename(req['filename'])
    except Exception as e:
        print(e)
        return "There was a fucky wucky"
    return "Yay!"
#####


def main():
    # setup access to the *real* webcam
    cap = cv2.VideoCapture('/dev/video0')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, 60)

    # setup the fake camera
    fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

    # load the image and scale it so we can use it immediately
    background = change_background(background_filename)

    # easy way to check for changes
    old_bg = background_filename

    print("Starting camera app")

    # frames forever
    while True:
        if background_filename != old_bg:
            print(f"Reloading to use {background_filename} from {old_bg}")
            background = change_background(background_filename)
            old_bg = background_filename
        next_frame = get_frame(cap, next(background))

        # fake webcam expects RGB
        next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)
        fake.schedule_frame(next_frame)



if __name__ == "__main__":
    # Load Flask
    kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}
    flaskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()
    # Load Camera
    main()

