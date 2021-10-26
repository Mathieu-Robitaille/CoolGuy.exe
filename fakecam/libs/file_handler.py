import filetype
import os
import sys
import imageio
import cv2
import urllib
import pathlib
import numpy as np

from libs import media


IS_DEBUG = False

def validate_path( path: str) -> bool:
    if not os.path.exists(path):
        if IS_DEBUG:
            print(f"Invalid path: {path}")
        return False
    if IS_DEBUG:
        print(f"Valid path: {path}")
    return True

def get_background_path(file: str):
    # Return a bool and the path
    # True if the path exists
    root_path = pathlib.Path(sys.modules['__main__'].__file__).resolve().parent
    background_path = os.path.join(root_path, 'backgrounds', file)
    return validate_path(background_path), background_path

# rewrite

def load_gif(uri: str) -> np.array:
    try:
        data = imageio.mimread(uri)
        if IS_DEBUG:
            print(f"file_handler.load_gif data: {data}")
    except Exception as e:
        print(f"Failed to load gif: {uri}")
        print(e)
        return None
    gif = media.Gif(data)
    if IS_DEBUG:
        print(f"file_handler.load_image media: {gif}")
    return gif

def load_image(uri: str) -> np.array:
    data = cv2.imread(uri)
    if IS_DEBUG:
        print(f"file_handler.load_image data: {data}")
    image = media.Image(media=data)
    if IS_DEBUG:
        print(f"file_handler.load_image media: {image}")
    return image

def load_background(uri: str) -> media.Media_Type:
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


def download_object(url: str, filename: str) -> None:
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
