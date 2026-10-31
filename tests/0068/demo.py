# The median of a stream with two heaps, the p-quantile by the nearest rank, and the
# quantile over the last W values
from solution import *  # noqa: F401,F403

stream = [5, 15, 1, 3, 8, 7, 9, 10, 20, 2]
print("medians:", stream_medians(stream))  # [5, 10.0, 5, 4.0, 5, 6.0, 7, 7.5, 8, 7.5]
print("p = 0.9:", stream_quantiles(stream, 9, 10))  # [5, 15, 15, 15, 15, 15, 15, 15, 20, 15]
print("p = 0.25:", stream_quantiles(stream, 1, 4))  # [5, 5, 1, 1, 3, 3, 3, 3, 5, 3]
print("p = 0 (the minimum):", stream_quantiles(stream, 0, 1))  # [5, 5, 1, 1, 1, 1, 1, 1, 1, 1]
print("W = 4, p = 0.5:", window_quantiles(stream, 4, 1, 2))  # [5, 5, 5, 3, 3, 3, 7, 8, 9, 9]
print("W = 4, p = 1 (the window's maximum):", window_quantiles(stream, 4, 1, 1))  # [5, 15, 15, 15, 15, 8, 9, 10, 20, 20]
