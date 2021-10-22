import cv2
import numpy as np
from abc import ABC, abstractmethod
from itertools import cycle

class Media_Type:
    def __init__(self) -> None:
        pass
    
    def resize(self):
        pass

    def __next__(self):
        if not isinstance(self.media, cycle):
            self.media = cycle(self.media)
    
    def test():
        pass


class Image(Media_Type):
    def __init__(self, media: np.array) -> None:
        self.media = media
            
    def resize(self, width, height) -> None:
        self.media = cv2.resize(self.media, (width, height))

    def __next__(self):
        return super().__next__()

class Gif(Media_Type):
    def __init__(self, media: np.array) -> None:
        self.media = media

    def resize(self, width, height) -> None:
        # I dont think we need to change the color?
        # conv_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif]
        self.media = [cv2.resize(frame, (width, height)) for frame in self.media]

    def __next__(self):
        return next(self.media)
