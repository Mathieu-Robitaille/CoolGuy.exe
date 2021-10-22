import cv2
import effects
import imageio
import os
import urllib.request
import numpy as np

from libs import file_handler


class Image_Handler:
    def __init__(
            self,
            width: int = 1280,
            height: int = 720,
            background_filename: str = "rat.gif",
            effect: effects.available_effects = effects.available_effects.no_effect
    ) -> None:
        self.width = width
        self.height = height

        self.background_filename = background_filename

        # This should be set to an iterator, preferably a cycle
        self.background = None

        self.effect = effect

    def change_effect(self, new_effect: effects.available_effects) -> None:
        self.effect = new_effect

    def apply_effect(self, frame: np.array) -> np.array:
        if self.effect == effects.available_effects.no_effect:
            pass
        return effects.apply_effect(frame, self.effect)

    def refine_mask(self, mask: np.array) -> np.array:
        mask = cv2.dilate(mask.astype('uint8'), np.ones((10, 10), np.uint8), iterations=1)
        mask = cv2.blur(mask.astype(float), (30, 30))
        return mask

    def composite_frames(self, capture: np.array, mask: np.array) -> np.array:
        inv_mask = 1 - mask
        bg = next(self.background)
       
        # How can I fix this?
        for c in range(capture.shape[2]):
            capture[:, :, c] = capture[:, :, c] * mask + bg[:, :, c] * inv_mask
        return capture

    #==================
    # Handle changing background
    #==================

    def change_background(self, filename: str) -> None:
        result, path = file_handler.get_background_path(filename)
        if not result:
            pass
        self.background_path = filename
        bg = file_handler.load_background(path)
        

    #==================
    # Somethign that shouldnt be here
    #==================

