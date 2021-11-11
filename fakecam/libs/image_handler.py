import cv2
import numpy as np

from itertools import cycle
from typing import Tuple

from libs import file_handler
from libs import effects
from libs import timer

class Image_Handler:
    def __init__(
            self,
            size: Tuple = (640, 480), # size: Tuple = (1280, 720),
            background_filename: str = "rat.gif",
            effect: effects.available_effects = effects.available_effects.no_effect,
            debug = False
    ) -> None:
        self.size = size
        self.background_filename = background_filename

        # This should be set to an iterator, preferably a cycle
        self.background = None
        self.effect = effect

        self.debug = debug

    def change_effect(self, new_effect: effects.available_effects) -> None:
        self.effect = new_effect

    @timer.time_func
    def apply_effect(self, frame: np.array) -> np.array:
        if self.effect == effects.available_effects.no_effect:
            pass
        return effects.apply_effect(frame, self.effect)

    @timer.time_func
    def refine_mask(self, mask: np.array) -> np.array:
        mask = cv2.dilate(mask.astype('uint8'), np.ones((10, 10), np.uint8), iterations=1)
        mask = cv2.blur(mask.astype(float), (20, 20))
        return mask

    #==================
    # Do a war crime
    #==================

    # Cleaner but slower composite
    @timer.time_func
    def cleaner_composite(self, capture: np.array, mask: np.array) -> np.array:
        mask = np.dstack([mask, mask, mask])
        inv_mask = 1 - mask
        bg = next(self.background)

        frame = capture * mask + bg * inv_mask
        return frame

    @timer.time_func
    def composite_frames(self, capture: np.array, mask: np.array) -> np.array:
        inv_mask = 1 - mask
        bg = next(self.background)
        
        if self.debug:
            for i in [capture, mask, inv_mask, bg]:
                print(f"Shapes: {i.shape}")
        
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
        if bg is None:
            pass
        bg.resize(self.size)
        self.background = cycle(bg.media)
