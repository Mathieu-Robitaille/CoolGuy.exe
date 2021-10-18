import cv2
import effects
import imageio
import os
import urllib.request
import numpy as np

from itertools import cycle


class Image_Handler:
    def __init__(
            self,
            width: int = 1280,
            height: int = 720,
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

    def change_effect(self, new_effect: effects.available_effects) -> None:
        self.effect = new_effect

    def apply_effect(self, frame):
        if self.effect == effects.available_effects.no_effect:
            pass
        return effects.apply_effect(frame, self.effect)

    def refine_mask(self, mask):
        mask = np.array(mask)
        mask = cv2.dilate(mask.astype('uint8'), np.ones((10, 10), np.uint8), iterations=1)
        mask = cv2.blur(mask.astype(float), (30, 30))
        return mask

    def composite_frames(self, capture: np.array, mask: np.array) -> np.array:
        inv_mask = 1 - mask
        bg = next(self.background)
        # Have fun :)
        for c in range(capture.shape[2]):
            capture[:, :, c] = capture[:, :, c] * mask + bg[:, :, c] * inv_mask
        return capture

    def load_gif(self, uri):
        gif = imageio.mimread(uri)
        conv_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif]
        scaled_gif = np.array(
            [cv2.resize(frame, (self.width, self.height)) for frame in conv_gif])
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
