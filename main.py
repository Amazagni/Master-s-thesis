from generators.shapes import ShapeGenerator
from utils.visualization import save_image
from noise.salt_pepper import add_salt_and_pepper_noise
from noise.gaussian import add_gaussian_noise
from noise.blur import add_blur
from noise.morfology import *
from noise.geometric_transformations import *
# from noise.geometric_transformations import rotate_image
# from noise.geometric_transformations import translate_image

gen = ShapeGenerator(seed=42)

shape_generators = {
    "circle": gen.generate_circle,
    "rectangle": gen.generate_rectangle,
    "triangle": gen.generate_triangle,
    "ring": gen.generate_ring,
}


noise_functions = {

    # noise
    "salt_pepper": lambda img: add_salt_and_pepper_noise(img, 0.20, 42), # TODO stopnie
    "gaussian": lambda img: add_gaussian_noise(img, 0.30, 42), # TODO sigma

    # blur
    "blur": lambda img: add_blur(img),

    # morphology
    "erode": lambda img: erode(img),
    "dilate": lambda img: dilate(img),

    # rotation
    "rotate_15": lambda img: rotate_image(img, 15),# TODO rozne wartosci (i losowe random_rotation)
    "rotate_30": lambda img: rotate_image(img, 30),
    "rotate_45": lambda img: rotate_image(img, 45),

    # scaling
    "scale_08": lambda img: scale_image(img, 0.8), # Nie wiem czy to bedzie potrzebne...
    "scale_12": lambda img: scale_image(img, 1.2),

    # translation
    "translate_small": lambda img: translate_image(img, 15, 10), # Tez nie wiem czy bedzie potrzebne
    "translate_big": lambda img: translate_image(img, 40, 30),
}

for shape_name, shape_func in shape_generators.items():

    img, meta = shape_func()

    save_image(img, f"results/images/{shape_name}_clean.png")

    for noise_name, noise_func in noise_functions.items():

        noisy_img = noise_func(img)

        save_image(
            noisy_img,
            f"results/images/{shape_name}_{noise_name}.png"
        )

print("Zapisano wszystkie obrazy.")