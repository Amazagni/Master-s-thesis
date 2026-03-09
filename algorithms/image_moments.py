import numpy as np


def raw_moments(image: np.ndarray):

    h, w = image.shape

    M00 = 0
    M10 = 0
    M01 = 0
    M11 = 0
    M20 = 0
    M02 = 0

    for y in range(h):
        for x in range(w):

            val = int(image[y, x])

            if val == 0:
                continue

            M00 += val
            M10 += x * val
            M01 += y * val
            M11 += x * y * val
            M20 += (x**2) * val
            M02 += (y**2) * val

    return {
        "M00": M00,
        "M10": M10,
        "M01": M01,
        "M11": M11,
        "M20": M20,
        "M02": M02,
    }
    
def centroid(moments):

    M00 = moments["M00"]

    if M00 == 0:
        return None

    cx = moments["M10"] / M00
    cy = moments["M01"] / M00

    return cx, cy

def central_moments(image, cx, cy): # odporne na translacje

    h, w = image.shape

    mu11 = 0
    mu20 = 0
    mu02 = 0

    for y in range(h):
        for x in range(w):

            val = int(image[y, x])

            if val == 0:
                continue

            dx = x - cx
            dy = y - cy

            mu11 += dx * dy * val
            mu20 += dx**2 * val
            mu02 += dy**2 * val

    return {
        "mu11": mu11,
        "mu20": mu20,
        "mu02": mu02,
    }
    
def normalized_central_moments(mu, M00):

    eta11 = mu["mu11"] / (M00 ** 2)
    eta20 = mu["mu20"] / (M00 ** 2)
    eta02 = mu["mu02"] / (M00 ** 2)

    return {
        "eta11": eta11,
        "eta20": eta20,
        "eta02": eta02
    }
    
def hu_moments(eta):

    n20 = eta["eta20"]
    n02 = eta["eta02"]
    n11 = eta["eta11"]

    hu1 = n20 + n02

    hu2 = (n20 - n02)**2 + 4*(n11**2)

    # uproszczone (bo nie liczymy jeszcze wyższych momentów)
    hu3 = n20 * n02 - n11**2

    return {
        "hu1": hu1,
        "hu2": hu2,
        "hu3": hu3
    }
    
def log_transform(hu): # todo podobno potrzebne, sprawdzic co to

    transformed = {}

    for k, v in hu.items():

        if v == 0:
            transformed[k] = 0
        else:
            transformed[k] = -np.sign(v) * np.log10(abs(v))

    return transformed