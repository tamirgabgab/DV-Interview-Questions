# Change n and k and press Run
for n in range(1, 17):
    print(f"n={n:2}  binary={n:5b}  simulation={josephus_sim(n):2}  formula={josephus_formula(n):2}  bits={josephus_bits(n):2}")

print()
print("41 people, every third leaves:", josephus_k(41, 3))
print("n = 10**6, k = 2, without simulation:", josephus_formula(10**6))
