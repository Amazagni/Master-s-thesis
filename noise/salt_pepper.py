import numpy as np


def add_salt_and_pepper_noise(image: np.ndarray, noise_level: float, seed: int | None = None):
    """
    image: obraz binarny (0/1)
    noise_level: prawdopodobieństwo zmiany piksela (np. 0.05 = 5%)
    seed: dla powtarzalności
    """

    if seed is not None:
        np.random.seed(seed)

    noisy = image.copy()

    # losowa macierz [0,1)
    random_matrix = np.random.rand(*image.shape)

    # pepper (ustaw na 0)
    noisy[random_matrix < noise_level / 2] = 0

    # salt (ustaw na 1)
    noisy[random_matrix > 1 - noise_level / 2] = 1

    return noisy