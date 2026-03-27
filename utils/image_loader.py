import numpy as np
from PIL import Image
from components.labeling import *

def load_image(path):
    """
    Wczytuje obraz i konwertuje do skali szarości (0-255)
    """

    img = Image.open(path).convert("L")  # grayscale
    img = np.array(img)

    return img

def to_binary(image, threshold=128):
    """
    Zamienia obraz grayscale na binarny (0/1)
    """

    binary = (image > threshold).astype(np.uint8)

    return binary

def otsu_threshold(image):
    """
    Prosta implementacja Otsu (bez bibliotek)
    """

    hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))

    total = image.size
    sum_total = np.dot(np.arange(256), hist)

    sum_b = 0
    w_b = 0
    max_var = 0
    threshold = 0

    for t in range(256):

        w_b += hist[t]
        if w_b == 0:
            continue

        w_f = total - w_b
        if w_f == 0:
            break

        sum_b += t * hist[t]

        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f

        var_between = w_b * w_f * (m_b - m_f) ** 2

        if var_between > max_var:
            max_var = var_between
            threshold = t

    return threshold


def to_binary_otsu(image):
    t = otsu_threshold(image)
    return (image > t).astype(np.uint8)


def load_and_prepare_image_otsu(path):

    img = load_image(path)

    binary = to_binary_otsu(img)

    cleaned = keep_largest_component(binary)
    
    cleaned = 1 - cleaned

    return cleaned


def load_and_prepare_image(path, threshold=128):

    img = load_image(path)

    binary = to_binary(img,  threshold=threshold)
    
    binary = 1 - binary
    
    return binary