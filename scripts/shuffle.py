import random


def read_qa_pairs(filename):
    with open(filename, "r") as f:
        content = f.read()

    # Split into QA pairs
    pairs = content.strip().split("\n\n")

    # Create list of (category, text) tuples
    qa_list = []
    for i in range(0, len(pairs), 1):
        pair = pairs[i].strip()
        if pair:
            lines = pair.split("\n")
            if (
                len(lines) >= 2
                and lines[0].startswith("category:")
                and lines[1].startswith("text:")
            ):
                qa_list.append((lines[0], lines[1]))

    return qa_list


def write_qa_pairs(filename, qa_pairs):
    with open(filename, "w") as f:
        for i, (category, text) in enumerate(qa_pairs):
            f.write(f"{category}\n{text}\n")
            if i < len(qa_pairs) - 1:
                f.write("\n")


# Read QA pairs
qa_pairs = read_qa_pairs("data/architecture.txt")

# Shuffle pairs
random.shuffle(qa_pairs)

# Write shuffled pairs back
write_qa_pairs("data/architecture.txt", qa_pairs)
