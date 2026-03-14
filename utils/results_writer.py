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
            "orientation"
        ])


def append_result(path, row):

    with open(path, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(row)