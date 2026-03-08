import numpy as np
from noise.morfology import erode


def extract_contour(image: np.ndarray):

    eroded = erode(image)

    contour = image - eroded

    contour[contour < 0] = 0

    return contour