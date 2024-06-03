import numpy as np
import scipy

__sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
__sy = __sx.T


def __cut_below(image, threshold):
    res = image.clip(0, 1)
    res[res <= threshold] = 0
    res[res > threshold] = 1
    return res


def __convolve_and_cut(image, kernel, threshold):
    res = scipy.ndimage.convolve(image, kernel)
    return __cut_below(res, threshold)


def sobel(image, threshold, axis):
    res = image.copy()
    if axis == 'x':
        return __convolve_and_cut(res, __sx, threshold)
    elif axis == 'y':
        return __convolve_and_cut(res, __sy, threshold)
    elif axis == 'all':
        h = scipy.signal.convolve2d(res, __sx)
        v = scipy.signal.convolve2d(res, __sy)
        res = np.sqrt(h ** 2 + v ** 2)
        return __cut_below(res, threshold)
    else:
        raise ValueError(f'Invalid axis: {axis}, must be one of {available_axis()}')


def available_axis():
    return ['x', 'y', 'all']
