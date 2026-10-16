# Change the values and press Run
N, M, MAX_SHAPES = 10, 8, 6


def draw(shapes):
    """Each unit cell shows the number of the shape that covers it."""
    for y in range(M - 1, 0, -1):                      # top row first
        row = ""
        for x in range(1, N):
            owner = [k + 1 for k, (x1, y1, x2, y2) in enumerate(shapes)
                     if x1 <= x < x2 and y1 <= y < y2]
            row += f"{owner[0]} " if owner else ". "
        print(row)


for squares in (True, False):
    shapes = random_shapes(N, M, MAX_SHAPES, squares=squares)
    print("squares:" if squares else "rectangles:", shapes)
    print("legal:", shapes_ok(N, M, shapes, squares))
    draw(shapes)
    print()
