# Rotate a 3 x 3 image, and transpose 2 x 3 in place, with and without marks
from solution import *  # noqa: F401,F403

img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate90(img)
print(img)  # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
a = ["a", "b", "c", "d", "e", "f"]
transpose(a, 2, 3)
print(a)  # ['a', 'd', 'b', 'e', 'c', 'f']
b = list(range(15))
transpose_no_marks(b, 3, 5)
print(b)  # [0, 5, 10, 1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 14]
