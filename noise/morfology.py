import numpy as np

def erode(image: np.ndarray):    
    """
    image: obraz binarny (0/1)
    sigma: odchylenie standardowe szumu (im wieksze tym dalej lądujemy)
    seed: dla powtarzalności
    """
    padded = np.pad(image, 1, mode="constant")

    eroded = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+3, j:j+3]
            eroded[i, j] = np.min(region)

    return eroded

def dilate(image: np.ndarray):
    """
    image: obraz binarny (0/1)
    sigma: odchylenie standardowe szumu (im wieksze tym dalej lądujemy)
    seed: dla powtarzalności
    """
    padded = np.pad(image, 1, mode="constant")

    dilated = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+3, j:j+3]
            dilated[i, j] = np.max(region)

    return dilated