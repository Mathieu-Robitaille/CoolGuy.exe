
import validators
import os
import sys
import time

from flask import Flask, request
from threading import Thread

from multiprocessing import Lock

working_dir = os.path.dirname(__file__)
libs_dir = os.path.join(working_dir, 'libs')
sys.path.append(libs_dir)

from bodypix import BodyPix
from camera import Camera, CameraCaptureError
from image_handler import Image_Handler
from effects import available_effects


import traceback

# As per https://stackoverflow.com/questions/28423069/store-large-data-or-a-service-connection-per-flask-session
ih_connection = None
flask_app = Flask(__name__)
lock = Lock()

default_image='popcorn.gif'

# Dont actually need to lock this...
def get_ih() -> Image_Handler:
    with lock:
        global ih_connection
        if not ih_connection:
            absolute_dir = os.path.abspath(os.path.dirname(__file__))
            ih_connection = Image_Handler(
                background_root_path=os.path.join(absolute_dir, 'backgrounds'),
                background_path=default_image
            )
        return ih_connection



# =======================
#  Move flask stuff to another file
# =======================

@flask_app.route('/', methods=['POST'])
def change_on_request():
    ih = get_ih()
    try:
        req = request.get_json()
        download_status = True
        if 'url' in req and 'filename' in req:
            if validators.url(req['url']):
                download_status = ih.download_object(req['url'], req['filename'])
        if 'filename' in req and download_status:
            ih.change_background(req['filename'])
    except Exception as e:
        print(e)
        return "There was a fucky wucky\n"
    return f"Changed to {req['filename']}!\n"

def start_flask():
    # Init Flask
    kwargs = {'host': '127.0.0.1', 'port': 9987, 'threaded': True, 'use_reloader': False, 'debug': False}
    Thread(target=flask_app.run, daemon=True, kwargs=kwargs).start()

# =======================

def main():
    # This takes the longes to "warm up"
    bodypix = BodyPix()

    # We need to see what we're doing :)
    camera = Camera()
    
    # Set up the image handler
    ih = get_ih()
    ih.change_background(ih.background_path)

    # Start flask after pre flight is done    
    start_flask()

    # frames forever
    while True:
        try:
            frame = camera.get_frame()
            frame = ih.apply_effect(frame)

            mask = bodypix.get_mask(capture=frame)
            mask = ih.refine_mask(mask)

            composited_frame = ih.composite_frames(capture=frame, mask=mask)
            camera.schedule_frame(composited_frame)
        except CameraCaptureError as e:
            print("The camera failed to capture a frame.\n\tSleeping now for a few seconds.")
            time.sleep(3)
        except Exception as e:
            # The best way to handle exceptions is obviously to just catch them all :)
            time.sleep(1)
            print(e)
            print(traceback.format_exc())
            quit()


if __name__ == "__main__":
    main()

