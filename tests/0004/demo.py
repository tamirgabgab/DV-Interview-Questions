import random

# The labels on the boxes, and what is really inside (every label must be wrong)
labels = ["RED", "BLACK", "MIXED"]
content = ["BLACK", "MIXED", "RED"]


def draw(i):
    """The provided API: one random ball from box i."""
    if content[i] == "MIXED":
        return random.choice(["RED", "BLACK"])
    return content[i]


print("labels:           ", labels)
print("fix_labels_simple:", fix_labels_simple(list(labels)))  # ['BLACK', 'MIXED', 'RED']
print("fix_labels:       ", fix_labels(list(labels)))  # ['BLACK', 'MIXED', 'RED']
print("real content:     ", content)
