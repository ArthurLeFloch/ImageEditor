from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

import matplotlib.pyplot as plt
import numpy as np
import skimage

import io
import sys

from utils import legofier, sobel, convolution, grayscale, segment

app = Flask(__name__)
CORS(app)

PORT = 3000

MAX_PIXELS = 4096 * 4096
MAX_KERNEL_SIZE = 7
MAX_BILATERAL_KERNEL_SIZE = 11
MAX_LEGOFY_SIZE = 1000
MAX_SEGMENTS = 1000000
DEBUG = True

if len(sys.argv) > 1:
    DEBUG = False


def get_image():
    image_file = request.files['image']
    image = plt.imread(io.BytesIO(image_file.read()), format='PNG')

    if image.dtype == np.uint8:
        image = image.astype(float) / 255
    if len(image.shape) == 2:
        image = np.dstack((image, image, image, np.ones_like(image)))
    if image.shape[2] == 3:
        image = np.dstack((image, np.ones_like(image[:, :, 0])))

    return image


def get_channels(image):
    return image[:, :, 0], image[:, :, 1], image[:, :, 2], image[:, :, 3]


def exists_form_data(name):
    return name in request.form


def get_form_data(name, cls):
    if request.form.get(name) is None:
        return None
    res = None
    try:
        res = cls(request.form[name])
    except Exception:
        pass
    return res


def is_form_invalid(*args):
    return None in args


def is_too_big(image):
    return image.shape[0] * image.shape[1] > MAX_PIXELS


def return_image(image):
    image = image.clip(0, 1)
    image_io = io.BytesIO()
    plt.imsave(image_io, image, format='PNG')
    image_io.seek(0)
    return send_file(image_io, mimetype='image/png')


@app.route('/test', methods=['GET'])
@cross_origin()
def api_test():
    return 'API is working'


@app.route('/rotate', methods=['POST'])
@cross_origin()
def api_rotate():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    angle = -get_form_data('angle', int)
    padding = get_form_data('padding', str)
    if is_form_invalid(angle, padding):
        return 'Invalid form data', 400

    if padding == 'black':
        rgb = image[:, :, :3]
        alpha = image[:, :, 3]
        rotated_rgb = skimage.transform.rotate(rgb, angle, resize=True, mode='constant', cval=0)
        rotated_alpha = skimage.transform.rotate(alpha, angle, resize=True, mode='constant', cval=1)
        image = np.dstack((rotated_rgb, rotated_alpha))
    elif padding == 'white':
        image = skimage.transform.rotate(image, angle, resize=True, mode='constant', cval=1)
    elif padding == 'no_resize':
        image = skimage.transform.rotate(image, angle)
    elif padding == 'transparent':
        image = skimage.transform.rotate(image, angle, resize=True)
    else:
        return 'Invalid padding', 400

    return return_image(image)


@app.route('/flip', methods=['POST'])
@cross_origin()
def api_flip():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    axis = get_form_data('axis', str)
    if is_form_invalid(axis):
        return 'Invalid form data', 400

    if axis == 'horizontal':
        image = np.fliplr(image)
    elif axis == 'vertical':
        image = np.flipud(image)
    else:
        return 'Invalid axis', 400

    return return_image(image)


@app.route('/resize', methods=['POST'])
@cross_origin()
def api_resize():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    width = get_form_data('width', int)
    height = get_form_data('height', int)
    if is_form_invalid(width, height):
        return 'Invalid form data', 400

    image = skimage.transform.resize(image, (height, width))

    return return_image(image)


@app.route('/grayscale', methods=['POST'])
@cross_origin()
def api_grayscale():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    formula = get_form_data('formula', str)
    if is_form_invalid(formula):
        return 'Invalid form data', 400

    if formula not in grayscale.available_formulas():
        return f'Invalid formula: {formula}, must be one of {grayscale.available_formulas()}', 400

    image = grayscale.grayscale(image, formula)

    return return_image(image)


@app.route('/sobel', methods=['POST'])
@cross_origin()
def api_sobel():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    sobel_type = get_form_data('sobel_type', str)
    threshold = get_form_data('threshold', float)
    if is_form_invalid(sobel_type, threshold):
        return 'Invalid form data', 400

    if sobel_type not in sobel.available_axis():
        return 'Invalid sobel type', 400

    image = grayscale.grayscale(image)
    image = image[:, :, 0]
    image = sobel.sobel(image, threshold, sobel_type)
    image = np.dstack((image, image, image, np.ones_like(image)))

    return return_image(image)


@app.route('/convolution', methods=['POST'])
@cross_origin()
def api_convolution():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    kernel_type = get_form_data('kernel_type', str)
    kernel_size = get_form_data('kernel_size', int)
    if is_form_invalid(kernel_type, kernel_size):
        return 'Invalid form data', 400

    # Check if kernel size is not too crazy
    if kernel_size > MAX_KERNEL_SIZE:
        return f'Kernel size must be less than {MAX_KERNEL_SIZE}', 400

    if kernel_type == 'median':
        image = convolution.median(image, kernel_size)
    elif kernel_type == 'average':
        image = convolution.average(image, kernel_size)
    elif kernel_type == 'gaussian':
        sigma_x = get_form_data('sigma_x', float)
        sigma_y = get_form_data('sigma_y', float)
        if is_form_invalid(sigma_x, sigma_y):
            return 'Invalid form data', 400
        if sigma_x <= 0 or sigma_y <= 0:
            return 'Sigma must be greater than 0', 400
        image = convolution.gaussian(image, kernel_size, sigma_x, sigma_y)
    else:
        return 'Invalid kernel type', 400

    return return_image(image)


@app.route('/bilateral', methods=['POST'])
@cross_origin()
def api_bilateral():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    kernel_size = get_form_data('kernel_size', int)
    sigma_color = get_form_data('sigma_color', float)
    sigma_space = get_form_data('sigma_space', float)
    if is_form_invalid(kernel_size, sigma_color, sigma_space):
        return 'Invalid form data', 400

    if kernel_size > MAX_BILATERAL_KERNEL_SIZE:
        return f'Kernel size must be less than {MAX_BILATERAL_KERNEL_SIZE}', 400

    if sigma_color <= 0 or sigma_space <= 0:
        return 'Sigma must be greater than 0', 400

    image = convolution.bilateral(image, kernel_size, sigma_color, sigma_space)

    return return_image(image)


@app.route('/legofy', methods=['POST'])
@cross_origin()
def api_legofy():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    color_space = get_form_data('color_space', str)
    width = get_form_data('width', int)
    height = get_form_data('height', int)
    if is_form_invalid(width, height, color_space):
        return 'Invalid form data', 400

    if color_space not in legofier.available_color_spaces():
        return f'Invalid color space: {color_space}, must be one of {legofier.available_color_spaces()}', 400

    if width > MAX_LEGOFY_SIZE or height > MAX_LEGOFY_SIZE:
        return f'Width and height must be less than {MAX_LEGOFY_SIZE}', 400

    image = skimage.transform.resize(image, (height, width))
    image = image[:, :, :3]
    image = legofier.legofy(image, color_space)

    return return_image(image)


@app.route('/segment', methods=['POST'])
@cross_origin()
def api_segment():
    image = get_image()
    if is_too_big(image):
        return f'Image must have less than {MAX_PIXELS} pixels', 400

    color = get_form_data('color', str)
    n = get_form_data('n', int)
    if is_form_invalid(color, n):
        return 'Invalid form data', 400

    if n > MAX_SEGMENTS:
        return f'Number of segments must be less than {MAX_SEGMENTS}', 400

    if color == 'average':
        image = segment.average_segment(image, n)
    elif color == 'center':
        image = segment.center_segment(image, n)
    else:
        return 'Invalid segment type', 400

    return return_image(image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
