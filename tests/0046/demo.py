# Starting code of the run panel of question 0046: the page's Python code is loaded
# as solution.py; call its functions here.
from solution import *  # noqa: F401,F403

square_example = [[1, 0, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [0, 1, 1, 1, 1],
                  [1, 1, 1, 1, 0]]
rect_example = [[1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 0, 1]]
tri_example = [[1, 0, 0, 0, 0, 0, 1],
               [1, 1, 0, 0, 0, 1, 1],
               [1, 1, 1, 0, 1, 1, 1],
               [1, 1, 1, 1, 0, 1, 0],
               [0, 1, 0, 1, 1, 1, 1]]

print(largest_square(square_example))      # (9, (0, 2), (2, 4))
print(largest_rectangle(rect_example))     # (8, (0, 0), (1, 3))
print(largest_square(rect_example))        # (4, (0, 0), (1, 1))
print(largest_rectangle([[0, 0], [0, 0]])) # (0, None, None)
print(largest_triangle(tri_example))       # (10, (3, 0), (0, 0), (3, 3))
print(largest_triangle([[0, 1, 0],
                        [1, 1, 1]]))       # (3, (1, 1), (0, 1), (1, 0)): no pyramids
