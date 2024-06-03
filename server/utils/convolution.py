import cv2
import numpy as np
import scipy


def get_channels(image):
    return image[:, :, 0], image[:, :, 1], image[:, :, 2], image[:, :, 3]


def average(image, kernel_size):
    R, G, B, A = get_channels(image)
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    R = scipy.ndimage.convolve(R, kernel)
    G = scipy.ndimage.convolve(G, kernel)
    B = scipy.ndimage.convolve(B, kernel)
    return np.dstack((R, G, B, A))


def median(image, kernel_size):
    R, G, B, A = get_channels(image)
    R = scipy.signal.medfilt2d(R, kernel_size)
    G = scipy.signal.medfilt2d(G, kernel_size)
    B = scipy.signal.medfilt2d(B, kernel_size)
    return np.dstack((R, G, B, A))


def gaussian(image, kernel_size, sigma_x, sigma_y):
    R, G, B, A = get_channels(image)
    sigma = (sigma_x, sigma_y)
    R = scipy.ndimage.gaussian_filter(R, sigma=sigma, radius=kernel_size // 2)
    G = scipy.ndimage.gaussian_filter(G, sigma=sigma, radius=kernel_size // 2)
    B = scipy.ndimage.gaussian_filter(B, sigma=sigma, radius=kernel_size // 2)
    return np.dstack((R, G, B, A))


def bilateral(image, kernel_size, sigma_color, sigma_space):
    # Using cv2 for fast computation
    cv2_image = image[:, :, :3]
    cv2_image = (cv2_image * 255).astype(np.uint8)
    res = cv2.bilateralFilter(cv2_image, kernel_size, sigma_color, sigma_space)
    res = res.astype(float) / 255
    return np.dstack((res, image[:, :, 3]))
