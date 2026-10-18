# Change A, B and D and press Run
for A, B, D in [(7, 11, 15), (4, 7, 9), (7, 11, 4), (3, 5, 1)]:
    plan = solve(A, B, D)
    if plan is None:
        print(f"A={A} B={B} D={D}: cannot be measured from time 0")
    else:
        steps = ", ".join(f"t={t}: flip {act if act else 'nothing (wait)'}" for t, act in sorted(plan.items()))
        print(f"A={A} B={B} D={D}: {steps}")
