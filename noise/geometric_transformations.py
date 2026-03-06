import numpy as np


def random_rotation(image, seed=None):

    if seed is not None:
        np.random.seed(seed)

    angle = np.random.uniform(0, 360)

    return rotate_image(image, angle)


def rotate_image(image: np.ndarray, angle_deg: float):
    """
    image: obraz binarny (0/1)
    angle_deg: kąt w stopniach
    """

    angle = np.deg2rad(angle_deg)

    h, w = image.shape
    cx = w // 2
    cy = h // 2

    rotated = np.zeros_like(image)

    cos_a = np.cos(angle)
    sin_a = np.sin(angle)

    for y in range(h):
        for x in range(w):

            # współrzędne względem środka
            x_shift = x - cx
            y_shift = y - cy

            # odwrotna rotacja
            src_x = cos_a * x_shift + sin_a * y_shift
            src_y = -sin_a * x_shift + cos_a * y_shift

            src_x += cx
            src_y += cy

            src_x = int(round(src_x))
            src_y = int(round(src_y))

            if 0 <= src_x < w and 0 <= src_y < h:
                rotated[y, x] = image[src_y, src_x]

    return rotated


def translate_image(image: np.ndarray, tx: int, ty: int):
    """
    tx – przesunięcie w poziomie
    ty – przesunięcie w pionie
    """

    h, w = image.shape
    translated = np.zeros_like(image)

    for y in range(h):
        for x in range(w):

            src_x = x - tx
            src_y = y - ty

            if 0 <= src_x < w and 0 <= src_y < h:
                translated[y, x] = image[src_y, src_x]

    return translated


def scale_image(image: np.ndarray, scale: float):
    """
    scale > 1  powiększenie
    scale < 1  pomniejszenie
    """

    h, w = image.shape
    cx = w // 2
    cy = h // 2

    scaled = np.zeros_like(image)

    for y in range(h):
        for x in range(w):

            x_shift = x - cx
            y_shift = y - cy

            src_x = x_shift / scale
            src_y = y_shift / scale

            src_x += cx
            src_y += cy

            src_x = int(round(src_x))
            src_y = int(round(src_y))

            if 0 <= src_x < w and 0 <= src_y < h:
                scaled[y, x] = image[src_y, src_x]

    return scaled