import numpy as np
from noise.morfology import erode


def extract_contour(image: np.ndarray):

    eroded = erode(image)

    contour = image - eroded

    contour[contour < 0] = 0

    return contour

import numpy as np

def extract_contour_4_8(image: np.ndarray, connectivity: int = 4) -> np.ndarray:
    assert connectivity in (4, 8), "connectivity must be 4 or 8"

    img = (image > 0).astype(np.uint8)

    h, w = img.shape
    contour = np.zeros_like(img)

    # definicja sąsiedztwa
    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:  # 8
        neighbors = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    for y in range(h):
        for x in range(w):
            if img[y, x] == 0:
                continue

            for dy, dx in neighbors:
                ny, nx = y + dy, x + dx

                if ny < 0 or ny >= h or nx < 0 or nx >= w:
                    contour[y, x] = 1
                    break

                if img[ny, nx] == 0:
                    contour[y, x] = 1
                    break

    return contour