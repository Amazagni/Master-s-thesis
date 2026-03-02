import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass
class ShapeMetadata:
    shape_type: str
    parameters: Dict
    area_theoretical: float


class ShapeGenerator:
    def __init__(self, size: int = 256, margin: int = 20, seed: int | None = None):
        self.size = size
        self.margin = margin
        if seed is not None:
            np.random.seed(seed)

    def _empty_image(self):
        return np.zeros((self.size, self.size), dtype=np.uint8)


    def generate_circle(self, radius_range: Tuple[int, int] = (30, 80)):
        image = self._empty_image()

        radius = np.random.randint(*radius_range)

        cx = np.random.randint(self.margin + radius, self.size - self.margin - radius)
        cy = np.random.randint(self.margin + radius, self.size - self.margin - radius)

        y, x = np.ogrid[:self.size, :self.size]
        mask = (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2
        image[mask] = 1

        area_theoretical = np.pi * radius ** 2

        return image, ShapeMetadata(
            shape_type="circle",
            parameters={"center": (cx, cy), "radius": radius},
            area_theoretical=area_theoretical
        )

    def generate_rectangle(self, width_range=(40, 120), height_range=(40, 120)):
        image = self._empty_image()

        width = np.random.randint(*width_range)
        height = np.random.randint(*height_range)

        x0 = np.random.randint(self.margin, self.size - width - self.margin)
        y0 = np.random.randint(self.margin, self.size - height - self.margin)

        image[y0:y0 + height, x0:x0 + width] = 1

        area_theoretical = width * height

        return image, ShapeMetadata(
            shape_type="rectangle",
            parameters={
                "top_left": (x0, y0),
                "width": width,
                "height": height
            },
            area_theoretical=area_theoretical
        )

    def generate_triangle(self):
        image = self._empty_image()

        points = self._random_points(3)

        for y in range(self.size):
            for x in range(self.size):
                if self._point_in_triangle((x, y), points):
                    image[y, x] = 1

        area_theoretical = self._triangle_area(*points)

        return image, ShapeMetadata(
            shape_type="triangle",
            parameters={"points": points},
            area_theoretical=area_theoretical
        )

    def generate_ring(self, outer_range=(50, 90), thickness_range=(10, 30)):
        image = self._empty_image()

        r_outer = np.random.randint(*outer_range)
        thickness = np.random.randint(*thickness_range)
        r_inner = r_outer - thickness

        cx = np.random.randint(self.margin + r_outer, self.size - self.margin - r_outer)
        cy = np.random.randint(self.margin + r_outer, self.size - self.margin - r_outer)

        y, x = np.ogrid[:self.size, :self.size]
        dist_sq = (x - cx) ** 2 + (y - cy) ** 2

        mask_outer = dist_sq <= r_outer ** 2
        mask_inner = dist_sq <= r_inner ** 2

        image[mask_outer] = 1
        image[mask_inner] = 0

        area_theoretical = np.pi * (r_outer ** 2 - r_inner ** 2)

        return image, ShapeMetadata(
            shape_type="ring",
            parameters={
                "center": (cx, cy),
                "r_outer": r_outer,
                "r_inner": r_inner
            },
            area_theoretical=area_theoretical
        )


    def _random_points(self, n):
        points = []
        for _ in range(n):
            x = np.random.randint(self.margin, self.size - self.margin)
            y = np.random.randint(self.margin, self.size - self.margin)
            points.append((x, y))
        return points

    def _triangle_area(self, p1, p2, p3):
        return abs(
            p1[0]*(p2[1]-p3[1]) +
            p2[0]*(p3[1]-p1[1]) +
            p3[0]*(p1[1]-p2[1])
        ) / 2

    def _point_in_triangle(self, p, points):
        p1, p2, p3 = points
        A = self._triangle_area(p1, p2, p3)
        A1 = self._triangle_area(p, p2, p3)
        A2 = self._triangle_area(p1, p, p3)
        A3 = self._triangle_area(p1, p2, p)

        return abs(A - (A1 + A2 + A3)) < 1e-5