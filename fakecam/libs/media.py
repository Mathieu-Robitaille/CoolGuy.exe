import cv2
import numpy as np
from abc import ABC, abstractmethod

class Media_Type(ABC):

    @abstractmethod
    def resize(self):
        pass
    
    def __str__(self) -> str:
        pass

class Image(Media_Type):

    def __init__(self, media: np.array) -> None:
        self.media = media

    def resize(self, size) -> None:
        self.media = [cv2.resize(self.media, size)]

    def __str__(self) -> str:
        return self.media

class Gif(Media_Type):

    def __init__(self, media: np.array) -> None:
        self.media = media

    def resize(self, size) -> None:
        conv_gif = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in self.media]
        self.media = [cv2.resize(frame, size) for frame in conv_gif]

    def __str__(self) -> str:
        return str(self.media)

class Video(Media_Type):

    def __init__(self, media: np.array) -> None:
        self.media = media

    def resize(self, size):
        self.media = [cv2.resize(frame, size) for frame in self.media]

    def __str__(self) -> str:
        return self.media