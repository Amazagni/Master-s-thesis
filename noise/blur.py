import numpy as np


def add_blur(image: np.ndarray):
    """
    image: obraz binarny (0/1)
    blur oknem 3x3
    """

    padded = np.pad(image, 1, mode="constant")

    blurred = np.zeros_like(image, dtype=float)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+3, j:j+3]
            blurred[i, j] = np.mean(region)

    # powrót do binarnego
    blurred = (blurred > 0.5).astype(int)

    return blurred