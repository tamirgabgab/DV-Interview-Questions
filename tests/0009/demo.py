import random

# The example from the page: box b holds the note notes[b] (index 0 unused).
notes = [0, 7, 11, 15, 16, 13, 2, 12, 14, 4, 5, 6, 3, 1, 8, 9, 10]
# Or try a random arrangement:
# notes = [0] + random.sample(range(1, N + 1), N)


def cycles(notes):
    seen, out = set(), []
    for start in range(1, N + 1):
        if start not in seen:
            out.append(cycle_from(notes, start))
            seen.update(out[-1])
    return out


print("cycles before:", cycles(notes))
room = Room(notes)
helper(room)
print("swaps used:   ", MAX_SWAPS - room.swaps_left)
print("cycles after: ", cycles(room.look_all()))
print()

for me in range(1, N + 1):
    ok = find_my_note(room, me)
    print(f"person {me:2}: {'found' if ok else 'FAILED'} after {MAX_OPENS - room.opens_left} opens")

print("\neverybody wins:", play(notes))
