# Regular expressions are a powerful way to perform some computations
# on strings that otherwise would be quite difficult.

import re

# To get rid of single quotes in text, we replace contractions with
# full words. This way, any single quotes that remain are actual quotes.

replacements = (
      ( "doesn't", "does not" ),
      ( "don't", "do not" ),
      ( "you're", "you are" ),
      ( "i'm", "i am" ),
      ( "we're", "we are" ),
      ( "they're", "they are" ),
      ( "won't", "will not" ),
      ( "can't", "can not" ),
      ( "shan't", "shall not" ),
      ( "shouldn't", "should not" ),
      ( "mustn't", "must not" )
    )

# Precompile a regex machine to recognize word separators.

word_separators = re.compile("[^a-z]+")

# \\s turns to \s, which means any whitespace character
# + repetition one or more times
# | means or
# [0-9] any digit character
# [] character class, any one of the characters inside

# The dictionary of words that we shall build up as we see them.

words = {}

with open('warandpeace.txt', encoding="utf-8") as wap:
    for line in wap:
        if len(line) < 2: # skip empty lines
            continue
        # Lowercase everything and remove the trailing linebreak character.
        line = line.lower()[:-1]
        # Remove the contractions (see above).
        for (orig, repl) in replacements:
            line = line.replace(orig, repl)
        # Remove whatever other possessives might remain.
        line = re.sub(r"'s\b", "", line) # Raw strings are handy for regexes.
        line = re.sub(r"'ll\b", "", line)
        # Process the individual words in the line.
        for word in word_separators.split(line):
            if len(word) > 0:
                words[word] = words.get(word, 0) + 1

print("Here are some individual word counts.")
for w in ('prince', 'russia', 'you', 'supercalifragilisticexpialidocious'):
    print(f"The word {w!r} occurs {words.get(w, 0)} times.")

# Turn a dictionary into a list of its items as (key, value) tuples.
# We first sort these words into alphabetic order.
words_list_f = sorted(words.items(), reverse=True)
# Custom sorting with a key function that gives something that can
# be order compared. Now we sort in frequency order. Since the previous
# step sorted these words in alphabetical order, two words with same
# frequency count will remain in their alphabetical order.
words_list_f = sorted(words_list_f, key = (lambda p: p[1]), reverse = True)
# Extract the words into a separate lists, ignoring their counts.
words_list = [w for (w, c) in words_list_f]

print("\nHere are the 100 most frequent words in War and Peace:")
print(words_list[:100])

once = list(reversed([w for w in words_list if words[w] == 1]))
print(f"\n{len(once)} words occur exactly once in War and Peace:")
print(", ".join(once))