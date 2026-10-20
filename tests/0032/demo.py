# The plan found by BFS, and the ten safe states
plan = river_plan()
print("crossings:", " -> ".join("alone" if p is None else p for p in plan))
print("safe states:", [s for s in range(16) if river_safe(s)])
