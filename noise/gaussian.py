import numpy as np


def add_gaussian_noise(image: np.ndarray, sigma: float = 0.2, seed: int | None = None):
    """
    image: obraz binarny (0/1)
    sigma: odchylenie standardowe szumu (im wieksze tym dalej lądujemy)
    seed: dla powtarzalności
    """

    if seed is not None:
        np.random.seed(seed)

    noise = np.random.normal(0, sigma, image.shape)
    print(noise)
    noisy = image + noise

    # progowanie z powrotem do binarnego
    noisy = (noisy > 0.5).astype(int)

    return noisy

    """
    dodajemy losowe wartosci z rozkladu normalnego gdzie sigma to nasze odchylenie standardowe
    """
