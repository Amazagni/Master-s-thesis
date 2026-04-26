import csv
import os


def init_csv(path):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "shape",
            "noise",
            "area",
            "perimeter",
            "aspect_ratio",
            "circularity",
            "compactness",
            "eccentricity",
            "orientation",
            "feret_max",
            "feret_min",
            "feret_mean",
            "malinowska",
            "zwykly11",
            "centralny11",
            "znormalizowany11"
        ])
        # shape_name,
        # "clean",
        # A,
        # P,
        # ratio,
        # circ,
        # comp,
        # ecc,
        # theta,
        # feret,
        # mal

def append_result(path, row):

    with open(path, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(row)