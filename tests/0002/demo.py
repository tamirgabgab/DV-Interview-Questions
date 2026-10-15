# Change the values and press Run
for swap in (swap_temp, swap_arith, swap_xor):
    v = [5, 3]
    swap(v, 0, 1)
    print(f"{swap.__name__:<11} [5, 3] -> {v}")

# The pitfall: the same variable twice
for swap in (swap_temp, swap_arith, swap_xor):
    v = [9]
    swap(v, 0, 0)
    print(f"{swap.__name__:<11} same variable: [9] -> {v}")
