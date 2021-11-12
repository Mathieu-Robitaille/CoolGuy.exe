from enum import Enum, auto

import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw


class available_effects(Enum):
    no_effect = auto()
    canny = auto()
    laplacian = auto()
    lipstick = auto()

def effect_canny(frame):
    return cv2.Canny(frame,100,200)

def effect_laplacian(frame):
    return cv2.Laplacian(frame, cv2.CV_8UC3)

def effect_lipstick(frame):
    #RGBA
    lip_color = (150, 0, 0, 128)
    eye_liner_color = (0, 0, 0, 110)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame_rgb = small_frame[:, :, ::-1]

    face_landmarks_list = face_recognition.face_landmarks(small_frame_rgb)

    pil_image = Image.fromarray(frame)

    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')
        d.polygon(face_landmarks['top_lip'], fill=lip_color)
        d.polygon(face_landmarks['bottom_lip'], fill=lip_color)

        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=eye_liner_color, width=6)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=eye_liner_color, width=6)
        
    # Return them all
    return np.array(pil_image)


def apply_effect(frame, effect: available_effects):
    if effect == available_effects.no_effect:
        return frame
    if effect == available_effects.canny:
        return effect_canny(frame)
    if effect == available_effects.laplacian:
        return effect_laplacian(frame)
    if effect == available_effects.lipstick:
        return effect_lipstick(frame)