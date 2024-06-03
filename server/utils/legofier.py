from skimage.color import rgb2lab, rgb2luv

colors = [
    (254, 205, 6),  # Bright Yellow
    (255, 245, 121),  # Cool Yellow
    (245, 125, 32),  # Bright Orange
    (251, 171, 24),  # Flame Yellowish Orange
    (221, 26, 33),  # Bright Red
    (233, 93, 162),  # Bright Purple
    (246, 173, 205),  # Light Purple
    (182, 28, 126),  # Bright Reddish Violet
    (149, 118, 178),  # Medium Lavender
    (188, 165, 207),  # Lavender
    (76, 47, 146),  # Medium Lilac
    (2, 108, 184),  # Bright Blue
    (72, 158, 206),  # Medium Blue
    (103, 130, 151),  # Sand Blue
    (1, 57, 94),  # Earth Blue
    (0, 163, 218),  # Dark Azur
    (0, 190, 212),  # Medium Azur
    (193, 228, 218),  # Aqua
    (0, 175, 80),  # Bright Green
    (112, 148, 122),  # Sand Green
    (1, 146, 71),  # Dark Green
    (0, 75, 45),  # Earth Green
    (156, 201, 59),  # Bright Yellowish Green
    (130, 131, 83),  # Olive Green
    (106, 46, 20),  # Reddish Brown
    (221, 196, 142),  # Brick Yellow
    (149, 125, 97),  # Sand Yellow
    (173, 116, 71),  # Medium Nougat
    (59, 25, 16),  # Dark Brown
    (253, 195, 158),  # Light Nougat
    (166, 84, 36),  # Dark Orange
    (255, 255, 255),  # White
    (160, 160, 160),  # Medium Stone Grey
    (103, 103, 103),  # Dark Stone Grey
    (0, 0, 0),  # Black
    (195, 151, 56),  # Warm Gold
    (135, 140, 143),  # Silver Metallic
    (24, 158, 159),  # Bright Bluish Green
    (249, 108, 98),  # Vibrant Coral
]

rgb_colors = [(r / 255, g / 255, b / 255) for r, g, b in colors]
lab_colors = [rgb2lab([[r, g, b]])[0] for r, g, b in rgb_colors]
luv_colors = [rgb2luv([[r, g, b]])[0] for r, g, b in rgb_colors]


def __nearest_color(pixel, color_list):
    min_dist = float('inf')
    min_index = 0
    for i, color in enumerate(color_list):
        dist = sum((a - b) ** 2 for a, b in zip(pixel, color))
        if dist < min_dist:
            min_dist = dist
            min_index = i
    return rgb_colors[min_index]


def __legofy(out, color_list):
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = __nearest_color(out[i, j], color_list)
    return out


def legofy(image, color_space):
    if color_space == 'rgb':
        res = image.copy()
        color_list = rgb_colors
    elif color_space == 'luv':
        res = rgb2luv(image)
        color_list = luv_colors
    elif color_space == 'lab':
        res = rgb2lab(image)
        color_list = lab_colors
    else:
        raise ValueError(f'Invalid color space: {color_space}, must be one of {available_color_spaces()}')

    return __legofy(res, color_list)


def available_color_spaces():
    return ['rgb', 'luv', 'lab']
