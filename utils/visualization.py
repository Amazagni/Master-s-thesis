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
    
# def save_labels(labels, path, title=None):
#     os.makedirs(os.path.dirname(path), exist_ok=True)

#     plt.figure(figsize=(5, 5))

#     n_labels = labels.max() + 1
#     cmap = plt.cm.get_cmap("nipy_spectral", n_labels)

#     im = plt.imshow(labels, cmap=cmap, vmin=0, vmax=n_labels - 1)
#     plt.axis("off")

#     if title:
#         plt.title(title)

#     cbar = plt.colorbar(im, ticks=np.arange(n_labels))
#     cbar.ax.tick_params(labelsize=6)  # mniejsze liczby

#     plt.savefig(path, bbox_inches="tight", dpi=300)
#     plt.close()

def save_equivalent_ellipse(
    image,
    cx,
    cy,
    mu20,
    mu02,
    mu11,
    path,
    scale=2,
    title=None
):
    """
    Zapisuje obraz z nałożoną elipsą aproksymującą + osiami
    """

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # --- macierz kowariancji ---
    cov = np.array([
        [mu20, mu11],
        [mu11, mu02]
    ])

    # --- wartości własne i wektory ---
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    # sortowanie malejąco
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    lambda1, lambda2 = eigenvalues

    area = np.sum(image)
    if area == 0:
        return

    # --- długości osi ---
    r1 = scale * np.sqrt(lambda1 / area)
    r2 = scale * np.sqrt(lambda2 / area)

    # --- parametry elipsy ---
    t = np.linspace(0, 2*np.pi, 200)

    ellipse = np.array([
        r1 * np.cos(t),
        r2 * np.sin(t)
    ])

    ellipse_rot = eigenvectors @ ellipse

    x_ellipse = ellipse_rot[0, :] + cx
    y_ellipse = ellipse_rot[1, :] + cy

    # --- rysowanie ---
    plt.figure(figsize=(5, 5))
    plt.imshow(image, cmap="gray", vmin=0, vmax=1)

    # elipsa
    plt.plot(x_ellipse, y_ellipse, linewidth=2)

    # --- osie ---
    v1 = eigenvectors[:, 0]
    v2 = eigenvectors[:, 1]

    axis1 = v1 * r1
    axis2 = v2 * r2

    plt.plot(
        [cx - axis1[0], cx + axis1[0]],
        [cy - axis1[1], cy + axis1[1]],
        linewidth=2
    )

    plt.plot(
        [cx - axis2[0], cx + axis2[0]],
        [cy - axis2[1], cy + axis2[1]],
        linewidth=2
    )

    # centroid
    plt.scatter(cx, cy)

    plt.axis("off")

    if title:
        plt.title(title)

    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()