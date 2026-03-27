import numpy as np
from collections import deque


def connected_components(binary_image: np.ndarray, connectivity: int = 4):
    """
    Connected Component Labeling dla obrazu binarnego.

    Parameters
    ----------
    binary_image : np.ndarray
        obraz binarny (0/1)
    connectivity : int
        4 lub 8

    Returns
    -------
    labels : np.ndarray
        macierz etykiet komponentów
    num_components : int
        liczba komponentów
    components : dict
        słownik {label: [(y,x), ...]}
    """

    if connectivity not in (4, 8):
        raise ValueError("connectivity musi być 4 lub 8")

    h, w = binary_image.shape
    labels = np.zeros((h, w), dtype=np.int32)

    current_label = 1
    components = {}

    if connectivity == 4:
        neighbors = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]
    else:
        neighbors = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    for y in range(h):
        for x in range(w):

            if binary_image[y, x] == 1 and labels[y, x] == 0:

                queue = deque([(y, x)])
                labels[y, x] = current_label

                pixels = [(y, x)]

                while queue:

                    cy, cx = queue.popleft()

                    for dy, dx in neighbors:

                        ny = cy + dy
                        nx = cx + dx

                        if (
                            0 <= ny < h and
                            0 <= nx < w and
                            binary_image[ny, nx] == 1 and
                            labels[ny, nx] == 0
                        ):

                            labels[ny, nx] = current_label
                            queue.append((ny, nx))
                            pixels.append((ny, nx))

                components[current_label] = pixels
                current_label += 1

    num_components = current_label - 1

    return labels, num_components, components

from components.labeling import connected_components


def keep_largest_component(binary_image):

    labels, num, components = connected_components(binary_image, connectivity=8)

    if num == 0:
        return binary_image

    max_label = None
    max_size = 0

    for label, pixels in components.items():
        if len(pixels) > max_size:
            max_size = len(pixels)
            max_label = label

    result = np.zeros_like(binary_image)

    for (y, x) in components[max_label]:
        result[y, x] = 1

    return result