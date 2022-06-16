from enum import Enum, auto

import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw

from libs import timer
from libs import opts

class available_effects(Enum):
    no_effect = auto()
    canny = auto()
    laplacian = auto()
    lipstick = auto()


def effect_canny(frame):
    return cv2.Canny(frame, 100, 200)


def effect_laplacian(frame):
    return cv2.Laplacian(frame, cv2.CV_8UC3)


def effect_lipstick(frame):
    """Very bad code rn go away"""

    #BGRA
    if isinstance(opts.top_lip_color, tuple):
        if opts.top_lip_color[-1] == 0:
            return frame
        top_lip_color = opts.top_lip_color
    else:
        top_lip_color = next(opts.top_lip_color)
    
    if isinstance(opts.bottom_lip_color, tuple):
        if opts.bottom_lip_color[-1] == 0:
            return frame
        bottom_lip_color = opts.bottom_lip_color
    else:
        bottom_lip_color = next(opts.bottom_lip_color)

    eye_color = opts.eye_color

    scalar = opts.lipstick_scalar
    eye_liner_width = opts.eye_liner_width

    small_frame = cv2.resize(frame, (0, 0), fx=(1 / scalar), fy=(1 / scalar))
    small_frame_rgb = small_frame[:, :, ::-1]

    face_landmarks_list = face_recognition.face_landmarks(small_frame_rgb)
    
    pil_image = Image.fromarray(frame)

    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        le = face_landmarks['left_eye']
        re = face_landmarks['right_eye']
        tl = face_landmarks['top_lip']
        bl = face_landmarks['bottom_lip']

        # Rescale the points back for use with the large image
        top_lip = [(x * scalar, y * scalar) for (x, y) in tl]
        bottom_lip = [(x * scalar, y * scalar) for (x, y) in bl]
        
        left_eye = [
            [(x * scalar, y * scalar) for (x, y) in le],
            (le[0][0] * scalar, le[0][1] * scalar)
        ]
        right_eye = [
            [(x * scalar, y * scalar) for (x, y) in re],
            (re[0][0] * scalar, re[0][1] * scalar)
        ]

        # Draw on the image
        d.polygon(top_lip, fill=top_lip_color)
        d.polygon(bottom_lip, fill=bottom_lip_color)

        # Fuck up the eyeballs
        d.line(left_eye[0] + [left_eye[1]], fill=eye_color, width=eye_liner_width)
        d.line(right_eye[0] + [right_eye[1]], fill=eye_color, width=eye_liner_width)
        
    # Return them all
    return np.array(pil_image)

@timer.time_func
def apply_effect(frame, effect: available_effects):
    if effect == available_effects.no_effect:
        return frame
    if effect == available_effects.canny:
        return effect_canny(frame)
    if effect == available_effects.laplacian:
        return effect_laplacian(frame)
    if effect == available_effects.lipstick:
        return effect_lipstick(frame)