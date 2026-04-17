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

    return (perimeter ** 2) /  area


def orientation(mu20, mu02, mu11):
    """
    Orientacja głównej osi obiektu (radiany)
    """

    if mu20 == mu02:
        return 0

    theta = 0.5 * np.arctan2(2 * mu11, mu20 - mu02)

    return float(theta)


def eccentricity(mu20, mu02, mu11):
    """
    Ekscentryczność wg definicji momentowej:
    Ecc = a1 / a2

    zakres:
    - 1 → koło
    - >1 → obiekt wydłużony
    """

    # składniki pomocnicze
    common = mu20 + mu02
    diff = mu20 - mu02

    sqrt_term = np.sqrt(diff**2 + 4 * (mu11**2))

    # a1 >= a2
    a1 = common + sqrt_term
    a2 = common - sqrt_term

    # zabezpieczenie
    if a2 == 0:
        return float("inf")

    ecc = a1 / a2

    return float(ecc)

def feret_diameter(contour):
    """
    Maksymalna odległość między punktami konturu
    """

    ys, xs = np.nonzero(contour)

    points = np.column_stack((xs, ys))

    max_dist = 0.0

    for i in range(len(points)):
        for j in range(i + 1, len(points)):

            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]

            dist = dx * dx + dy * dy

            if dist > max_dist:
                max_dist = dist

    return float(np.sqrt(max_dist))
            
def malinowska(area, perimeter):
    """
    Współczynnik Malinowskiej (0 = koło)
    """

    if area == 0:
        return 0

    return (perimeter / (2 * np.sqrt(np.pi * area))) - 1