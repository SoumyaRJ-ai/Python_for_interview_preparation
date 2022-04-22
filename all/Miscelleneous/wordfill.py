import bisect
import random


# Recursively fill an n-by-n box of letters so that every row and
# every column is some n-letter word. The call finds all the
# possible ways to fill in the i:th horizontal word, given the
# previous i - 1 horizontal and vertical words. If babbage is
# set to True, the word square must have same rows and columns.
def wordfill(n, i, horiz, vert, wordlist, vv, babbage=False):
    # Entire square is complete when rows 0, ..., n-1 are filled.
    if i == n:
        yield horiz
    else:
        # Vertical words constrain the next horizontal word.
        prefix = "".join([w[i] for w in vert])
        # Find the first word that starts with that prefix.
        idx = bisect.bisect_left(wordlist, prefix)
        # Iterate over words that start with that prefix.
        while idx < len(wordlist) and wordlist[idx].startswith(prefix):
            word = wordlist[idx]
            # If not used yet, try using that word as the horizontal word.
            if not (word in horiz or word in vert):
                horiz.append(word)
                if babbage:
                    yield from wordfill(n, i + 1, horiz, horiz, wordlist, 0, True)
                else:
                    yield from wordfill(n, i + vv, vert, horiz, wordlist, 1 - vv)
                horiz.pop()
            idx += 1


if __name__ == "__main__":
    import itertools

    n = 5  # Size of each individual word square.

    with open("words_alpha.txt", encoding="utf-8") as f:
        wordlist = [x.strip() for x in f if x.islower()]
    print(f"Read in a word list of {len(wordlist)} words.")
    wordlist = sorted([x for x in wordlist if len(x) == n])
    print(f"There remain {len(wordlist)} words of length {n}.")

    wordset = set(wordlist)
    rows, cols = 3, 4
    result = []
    while len(result) < rows * cols:
        # The first word on the first row.
        w1 = random.choice(wordlist)
        # Find the section of words that start with same letter.
        i1 = bisect.bisect_left(wordlist, w1[0])
        i2 = bisect.bisect_right(wordlist, chr(ord(w1[0]) + 1))
        # Choose one of those words as the first vertical word.
        w2 = wordlist[random.randint(i1, i2 - 1)]
        for sol in itertools.islice(wordfill(n, 1, [w1], [w2], wordlist, 0), 1):
            result.append(sol)

    print(f"Printing out {rows * cols} random word squares.\n")
    print("-" * ((n + 3) * cols + 1))
    for row in range(rows):
        idx = row * cols
        for j in range(n):
            print("| ", end="")
            for i in range(idx, idx + cols):
                print(result[i][j], end=" | ")
            print("")
        print("-" * ((n + 3) * cols + 1))
