import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


import os


def save_image(image, path, title=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap="gray", vmin=0, vmax=1)
    plt.axis("off")

    if title:
        plt.title(title)

    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()
    
def save_binary_image_raw(image, path):
    """
    zapisuje dokładnie 256x256 bez skalowania
    """

    img = (image * 255).astype(np.uint8)

    im = Image.fromarray(img)

    im.save(path)

def show_image(image, title=None):
    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap="gray", vmin=0, vmax=1)
    plt.axis("off")
    if title:
        plt.title(title)
    plt.show()


def show_multiple(images, titles=None, cols=3):
    n = len(images)
    rows = (n + cols - 1) // cols

    plt.figure(figsize=(4 * cols, 4 * rows))

    for i, img in enumerate(images):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(img, cmap="gray", vmin=0, vmax=1)
        plt.axis("off")
        if titles:
            plt.title(titles[i])

    plt.tight_layout()
    plt.show()


def overlay_contour(image, contour_points):
    """
    image: obraz binarny
    contour_points: lista (x, y)
    """
    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap="gray", vmin=0, vmax=1)

    if contour_points:
        xs = [p[0] for p in contour_points]
        ys = [p[1] for p in contour_points]
        plt.plot(xs, ys, linewidth=1)

    plt.axis("off")
    plt.show()
    
    
def show_labels(labels, title=None):
    """
    Wizualizacja macierzy etykiet komponentów
    """

    plt.figure(figsize=(5, 5))
    plt.imshow(labels, cmap="nipy_spectral")
    plt.axis("off")

    if title:
        plt.title(title)

    plt.colorbar()
    plt.show()
    
def save_labels(labels, path, title=None):
    """
    Zapis wizualizacji komponentów do pliku
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.figure(figsize=(5, 5))
    plt.imshow(labels, cmap="nipy_spectral")
    plt.axis("off")

    if title:
        plt.title(title)

    plt.colorbar()

    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()