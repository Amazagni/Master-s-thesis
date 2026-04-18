from generators.shapes import ShapeGenerator
from utils.visualization import *
from noise.salt_pepper import add_salt_and_pepper_noise
from noise.gaussian import add_gaussian_noise
from noise.blur import add_blur
from noise.morfology import *
from components.labeling import *
from noise.geometric_transformations import *
from algorithms.contour_extraction import *
from algorithms.shape_descriptors import *
from algorithms.image_moments import *
from utils.results_writer import *
from utils.image_loader import *

gen = ShapeGenerator(seed=42)

shape_generators = {
    "circle": gen.generate_circle,
    "rectangle": gen.generate_rectangle,
    "triangle": gen.generate_triangle,
    "ring": gen.generate_ring,
}

real_images = {
    "building": "data/real/building_binary.png",
    "building_otsu": "data/real/building_binary_otsu.png",

    "face": "data/real/face_binary.png",
    "face_otsu": "data/real/face_binary_otsu.png",
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

csv_path = "results/descriptors.csv"

init_csv(csv_path)

# for shape_name, path in real_images.items():# TODO sprawdzic czy to dziala

#     img = load_image(path)
#     img = to_binary(img)

for shape_name, shape_func in shape_generators.items():

    img, meta = shape_func()

    save_image(img, f"results/images/{shape_name}_clean.png")
    contour = extract_contour(img)
    save_image(contour, f"results/images/{shape_name}_contour.png")
    A = area(img)
    P = perimeter(contour)
    print(np.max(img))  # TODO dodac repetition
    print(img.shape)  # TODO dodac repetition
    print(A)  # TODO dodac repetition

        
    feret = feret_diameter(contour)
    mal = malinowska(A, P)
    
    bbox = bounding_box(img)

    ratio = aspect_ratio(bbox["width"], bbox["height"])
    circ = circularity(A, P)
    comp = compactness(A, P)

    # save_image(contour, f"results/images/{shape_name}_contour.png")
    
    mom = raw_moments(img)
    cx, cy = centroid(mom)
    mu = central_moments(img, cx, cy)
    eta = normalized_central_moments(mu, mom["M00"])
    hu = hu_moments(eta)
    theta = orientation(
    mu["mu20"],
    mu["mu02"],
    mu["mu11"]
    )
    
    
    save_equivalent_ellipse(
    img,
    cx,
    cy,
    mu["mu20"],
    mu["mu02"],
    mu["mu11"],
    f"results/images/{shape_name}_ellipse.png",
    title="Equivalent ellipse"
    )

    ecc = eccentricity(
        mu["mu20"],
        mu["mu02"],
        mu["mu11"]
    )
    
    print(shape_name)
    print("Area:", mom["M00"])
    print("Centroid:", cx, cy)
    print("Hu moments:", hu)
    print("Orientation:", theta)
    print("Eccentricity:", ecc)
    
    append_result(
    csv_path,
    [
        shape_name,
        "clean",
        A,
        P,
        ratio,
        circ,
        comp,
        ecc,
        theta,
        feret,
        mal,
        mom["M11"],
        mu["mu11"],
        eta["eta11"],
    ]
)
    
    labels4, n4, _components4 = connected_components(img, connectivity=4) # TODO ma sens tylko jesli mam dwa obiekty...
    # labels8, n8, _components8 = connected_components(img, connectivity=8)
    
    save_labels(
        labels4,
        f"results/images/{shape_name}_labels4.png"
    )

    # save_labels(
    #     labels8,
    #     f"results/images/{shape_name}_labels8.png"
    # )
    
    for noise_name, noise_func in noise_functions.items():

        noisy_img = noise_func(img)

        save_image(
            noisy_img,
            f"results/images/{shape_name}_{noise_name}.png"
        )
        
        contour = extract_contour(noisy_img)

        mom = raw_moments(noisy_img)
        cx, cy = centroid(mom)

        if cx is None:
            continue

        mu = central_moments(noisy_img, cx, cy)
        
        eta = normalized_central_moments(mu, mom["M00"])

        theta = orientation(
            mu["mu20"],
            mu["mu02"],
            mu["mu11"]
        )

        ecc = eccentricity(
            mu["mu20"],
            mu["mu02"],
            mu["mu11"]
        )

        A = area(noisy_img)
        P = perimeter(contour)
        
        feret = feret_diameter(contour)
        mal = malinowska(A, P)

        bbox = bounding_box(noisy_img)

        ratio = aspect_ratio(bbox["width"], bbox["height"])
        circ = circularity(A, P)
        comp = compactness(A, P)
        
        labels4_noisy, n4_noisy, _components4 = connected_components(noisy_img, connectivity=4)
        labels8_noisy, n8_noisy, _components8 = connected_components(noisy_img, connectivity=8)
        append_result(
            csv_path,
            [
                shape_name,
                noise_name,
                A,
                P,
                ratio,
                circ,
                comp,
                ecc,
                theta,
                feret,
                mal,
                mom["M11"],
                mu["mu11"],
                eta["eta11"],
            ]
        )
        save_labels(
            labels4_noisy,
            f"results/images/{shape_name}_{noise_name}_labels4_noisy.png"
        )

        # save_labels(
        #     labels8_noisy,
        #     f"results/images/{shape_name}_{noise_name}_labels8_noisy.png"
        # )
        # if (n4_noisy != 1 or n8_noisy):
        #     print(f"Wiecej niz jedna figura: {shape_name}_{noise_name}")

print("Zapisano wszystkie obrazy.")  # TODO dodac repetition