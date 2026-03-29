from utils.visualization import *
from utils.image_loader import *

real_images = {
    # "face": "data/real/face.jpg",
    "building": "data/big/building.jpg",
}

for name, path in real_images.items():

    img = load_and_prepare_image_otsu(path)

    save_image(img, f"data/margin/{name}_binary_otsu.png")
    # save_binary_image_raw(img, f"data/real/{name}_binary_otsu.png")

    img = load_and_prepare_image(path)

    save_image(img, f"data/margin/{name}_binary.png")
    # save_binary_image_raw(img, f"data/real/{name}_binary.png")