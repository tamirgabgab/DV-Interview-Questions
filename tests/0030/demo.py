# The room of the question: 30 x 12 x 12, spider (0, 6, 11), fly (30, 6, 1)
d, exit_point = shortest_path(30, 12, 12, 6, 11, 6, 1)
print(f"distance {d:.4f}, the spider leaves its wall at {exit_point}")

# Move the fly up the wall and watch the best route change
for z1 in (1, 3, 5, 6, 8, 11):
    d, (x, y, z) = shortest_path(30, 12, 12, 6, 11, 6, z1)
    print(f"fly at z = {z1:2}: distance {d:7.4f}, exit at (0, {y:.2f}, {z:.2f})")

# A cube, centre of one face to the centre of the opposite face
print("cube:", shortest_path(1, 1, 1, 0.5, 0.5, 0.5, 0.5))  # (2.0, (0.0, 0.5, 0.0))
