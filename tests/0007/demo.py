import math
import random

# A few random triangles that contain the center
for _ in range(3):
    pts = random_triangle_with_center()
    print([(round(x, 3), round(y, 3)) for x, y in pts], "inside:", center_inside(pts))

# Estimate the probability for random angles (the answer is 1/4)
n = 100_000
hits = sum(contains_center([random.uniform(0, 2 * math.pi) for _ in range(3)]) for _ in range(n))
print(f"P(center inside) ~ {hits / n:.4f}")
