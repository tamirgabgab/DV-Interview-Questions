# Change A, B and D and press Run
for A, B, D in [(7, 11, 1), (7, 11, 4), (4, 7, 1), (7, 11, 15)]:
    result = solve(A, B, D)
    if result is None:
        print(f"A={A} B={B} D={D}: impossible")
        continue
    start, plan = result
    steps = ", ".join(f"t={t}: {'flip ' + act if act else 'wait'}" for t, act in sorted(plan.items()))
    print(f"A={A} B={B} D={D}: measure from {start} to {start + D}  |  {steps}")
