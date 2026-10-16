# Eurovision 2026 grand final: (country, jury, public). Change the numbers and press Run.
results = [
    ("Bulgaria", 204, 312), ("Israel", 123, 220), ("Romania", 64, 232),
    ("Australia", 165, 122), ("Italy", 134, 147), ("Finland", 141, 138),
    ("Denmark", 165, 78), ("Moldova", 43, 183), ("Ukraine", 54, 167),
    ("Greece", 73, 147), ("France", 144, 14), ("Poland", 133, 17),
    ("Albania", 60, 85), ("Norway", 115, 19), ("Croatia", 53, 71),
    ("Czechia", 104, 9), ("Serbia", 38, 52), ("Malta", 81, 8),
    ("Cyprus", 41, 34), ("Sweden", 35, 16), ("Belgium", 36, 0),
    ("Lithuania", 10, 12), ("Germany", 12, 0), ("Austria", 1, 5),
    ("United Kingdom", 1, 0),
]
PUBLIC_TOTAL = 36 * 58

order = sorted(results, key=lambda r: r[1])          # announced from the lowest jury score
me = next(i for i, r in enumerate(order) if r[0] == "Israel")
israel_total = order[me][1] + order[me][2]
above = order[me + 1:]
points_left = PUBLIC_TOTAL - sum(public for _, _, public in order[:me + 1])

print("Israel total:", israel_total, "| points left after Israel:", points_left)
for k in range(len(above) + 1):
    left = points_left - sum(public for _, _, public in above[:k])
    jury_left = [jury for _, jury, _ in above[k:]]
    passed = any(jury + public > israel_total for _, jury, public in above[:k])
    last = above[k - 1][0] if k else "Israel"
    print(f"after {last:10} left={left:4}  cannot win: {passed or israel_cannot_win(israel_total, jury_left, left)}")

k = earliest_certain_loss(israel_total, above, points_left)
print("\nearliest_certain_loss:", k, "->", above[k - 1][0] if k else "right after Israel")
