import cv2
from enum import Enum, auto

class available_effects(Enum):
    no_effect = auto()
    canny = auto()
    laplacian = auto()

def effect_canny(frame):
    return cv2.Canny(frame,100,200)

def effect_laplacian(frame):
    return cv2.Laplacian(frame, cv2.CV_8UC3)

def apply_effect(frame, effect: available_effects):
    if effect == available_effects.no_effect:
        return frame
    if effect == available_effects.canny:
        return effect_canny(frame)
    if effect == available_effects.laplacian:
        return effect_laplacian(frame)
