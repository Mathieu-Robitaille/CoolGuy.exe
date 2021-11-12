import cv2
import filetype
import imageio
import math
import os
import pathlib
import sys
import urllib
import numpy as np

from libs import media


IS_DEBUG = False

# Max file size to load im MB
MAX_SIZE = 20
# 30 sec of video should be enough at 60 fps (we're usually at 15 so 4x as long)
MAX_FRAMES_TO_LOAD = 1800

def validate_path( path: str) -> bool:
    if not os.path.exists(path):
        if IS_DEBUG:
            print(f"Invalid path: {path}")
        return False
    if IS_DEBUG:
        print(f"Valid path: {path}")
    return True

def get_background_path(file: str):
    # Return a bool and the path, True if the path exists
    # We get whr th main fil is just incase the working dir is messed up or something
    root_path = pathlib.Path(sys.modules['__main__'].__file__).resolve().parent
    background_path = os.path.join(root_path, 'backgrounds', file)
    return validate_path(background_path), background_path

def get_file_size(uri) -> int:
    return os.path.getsize(uri) / 2 ** 20

#==================
# File loaders
#==================

def load_video(uri: str) -> np.array:
    try:
        handler = cv2.VideoCapture(uri)
        if not handler.isOpened():
            return None
        # Make sure we eithr have enough frames or we dont over load
        num_frames = min(MAX_FRAMES_TO_LOAD, handler.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_buffer = []
        while len(frame_buffer) < num_frames:
            status, frame = handler.read()
            if not status:
                break
            frame_buffer.append(frame)
        video = media.Video(frame_buffer)
    except Exception as e:
        print("Large exception catch since we're not quite sure what could be thrown yet.")
        print("Throwing from video loader")
        print(e)
        return None
    finally:
        handler.release()
    return video

def load_gif(uri: str) -> np.array:
    try:
        data = imageio.mimread(uri)
        if IS_DEBUG:
            print(f"file_handler.load_gif data: {data}")
        gif = media.Gif(data)
    except Exception as e:
        print("Large exception catch since we're not quite sure what could be thrown yet.")
        print("Throwing from gif loader")
        print(e)
        return None
    return gif

def load_image(uri: str) -> np.array:
    try:
        data = cv2.imread(uri)
        if IS_DEBUG:
            print(f"file_handler.load_image data: {data}")
        image = media.Image(data)
        if IS_DEBUG:
            print(f"file_handler.load_image media: {image}")
    except Exception as e:
        print("Large exception catch since we're not quite sure what could be thrown yet.")
        print("Throwing from image loader")
        print(e)
        return None
    return image

#==================
# File loaders end
#==================

def load_background(uri: str) -> media.Media_Type:
    # If ever we load invalid data return None to signify we should not rload th background
    # This avoids crashing the app with garbage
    # Make sure you log it tho
    size = get_file_size(uri)
    if size > MAX_SIZE:
        if IS_DEBUG:
            print("file_handler.load_background Filesize too large.")
            print(f"URI: {uri}\nSize: {size}")
            print("refusing to load")
        return None

    kind = filetype.guess(uri)
    if IS_DEBUG:
        print(f"file_handler.load_background file: {uri}")
        print(f"file_handler.load_background extension: {kind.extension}")

    if kind.extension in ["gif"]:
        if IS_DEBUG:
            print("file_handler.load_background loading Gif")
        return load_gif(uri)

    if kind.extension in ["jpg", "png"]:
        if IS_DEBUG:
            print(f"file_handler.load_background loading Image")
        return load_image(uri)

    if kind.extension in ["mp4"]:
        if IS_DEBUG:
            print(f"file_handler.load_background loading mp4")
        return load_video(uri)

def download_object(url: str, filename: str) -> None:
    # Maybe use beautiful soup? to load the gif element
    # this could pose an issue with selecting the correct element
    result, path = get_background_path(filename)
    if result:
        pass
    try:
        data = bytearray(urllib.request.urlopen(url).read())
        with open(path, "wb+") as f:
            f.write(data)
    except Exception as e:
        print("This got caught by a large net.")
        print(e)
