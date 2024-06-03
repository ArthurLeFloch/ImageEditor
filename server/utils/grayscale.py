import numpy as np


def grayscale(image, formula='average'):
    R, G, B, A = image[:, :, 0], image[:, :, 1], image[:, :, 2], image[:, :, 3]

    if formula == 'average':
        val = (R + G + B) / 3
    elif formula == 'luminosity':
        val = 0.299 * R + 0.587 * G + 0.114 * B
    else:
        raise ValueError('Invalid formula')

    return np.dstack((val, val, val, A))


def available_formulas():
    return ['average', 'luminosity']
