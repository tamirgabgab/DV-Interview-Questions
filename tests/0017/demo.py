# Change the array (n + 1 values between 1 and n) and press Run
nums = [3, 9, 5, 6, 7, 8, 1, 1, 2, 4]

for f in (find_duplicate_sort, find_duplicate_seen, find_duplicate_binary, find_duplicate_floyd):
    print(f"{f.__name__:22} -> {f(nums)}")

# The walk from index 0: the tail, then the cycle
x, path = 0, [0]
for _ in range(10):
    x = nums[x]
    path.append(x)
print("walk from 0:", " -> ".join(map(str, path)))
