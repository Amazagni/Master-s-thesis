from generators.shapes import ShapeGenerator
from utils.visualization import save_image

gen = ShapeGenerator(seed=42)

img, meta = gen.generate_circle()

save_image(
    img,
    "results/images/circle_test.png",
    title="Circle"
)

print("Zapisano obraz.")