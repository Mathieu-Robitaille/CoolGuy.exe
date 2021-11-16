import colorsys

def color_rainbow():
    n = 1
    while True:
        yield tuple(round(i * 255) for i in colorsys.hsv_to_rgb(n / 360, 1, 1))
        n = (n + 1) % 360

config = {
    "final_size": [1280, 720],
    "camera_size": [640, 480],

    "effects": {
        "makeup": {
            "eye_liner_width": 2,
            "lipstick_scalar": 4
        }
    }
}


rainbow_gen = color_rainbow()

#BGRA
colors = {
    "black": (0, 0, 0, 110),
    "pink": (203, 192, 255, 128),
    "red": (0, 0, 150, 128),
    "blue": (150, 0, 0, 128),
    "transparent": (0, 0, 0, 0),
    "rainbow": rainbow_gen
}

eye_liner_width = config["effects"]["makeup"]["eye_liner_width"]
lipstick_scalar = config["effects"]["makeup"]["lipstick_scalar"]

eye_color = colors["transparent"]


top_lip_color = colors["rainbow"]
bottom_lip_color = colors["rainbow"]

