import numpy as np


def area(image):
    """
    Pole powierzchni obiektu
    """
    return int(np.sum(image))


def perimeter(contour):
    """
    Obwód obiektu (liczba pikseli konturu)
    """
    return int(np.sum(contour))


def bounding_box(image):
    """
    Prostokąt otaczający obiekt
    """

    ys, xs = np.nonzero(image)

    min_x = xs.min()
    max_x = xs.max()

    min_y = ys.min()
    max_y = ys.max()

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return {
        "min_x": int(min_x),
        "max_x": int(max_x),
        "min_y": int(min_y),
        "max_y": int(max_y),
        "width": int(width),
        "height": int(height)
    }


def aspect_ratio(width, height):
    """
    Stosunek szerokości do wysokości
    """
    if height == 0:
        return 0

    return width / height


def circularity(area, perimeter):
    """
    Miara podobieństwa do koła
    """

    if perimeter == 0:
        return 0

    return (4 * np.pi * area) / (perimeter ** 2)


def compactness(area, perimeter):
    """
    Zwartość obiektu
    """

    if area == 0:
        return 0

    return (perimeter ** 2) / (4 * np.pi * area)