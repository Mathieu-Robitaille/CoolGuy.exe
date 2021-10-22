import re
import filetype
import os
import sys
import imageio
import cv2

import urllib

import pathlib

import numpy as np

from itertools import cycle

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
    root_path = pathlib.Path(sys.modules['__main__'].__file__).resolve().parent
    background_path = os.path.join(root_path, 'backgrounds', file)
    return validate_path(background_path), background_path


# rewrite

def load_gif(uri: str) -> np.array:
    try:
        gif = media.Gif(np.array(imageio.mimread(uri)))
    except Exception as e:
        print(f"Failed to load gif: {uri}")
        print(e)
        return None
    return gif

def load_image(uri: str) -> np.array:
    return media.Image(cv2.imread(uri))

def load_background(uri: str) -> media.Media_Type:
    kind = filetype.guess(uri)
    if kind.extension in ["gif"]:
        if IS_DEBUG:
            print("loading Gif")
        return load_gif(uri)
    if kind.extension in ["jpg", "png"]:
        if IS_DEBUG:
            print(f"loading image {uri}")
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
