# Strings in Code

## The idea
Think of a row of Scrabble tiles spelling out a sentence. Every letter is its own tile. So is every space, every full stop and every digit. You can count the tiles, or split the row into words wherever there's a gap.

In Python, text works the same way. A piece of text is called a **string**: a row of characters, written inside quotes. A **character** is any single tile in that row, including spaces and punctuation.

## The project: LinkedIn Post Character Counter
LinkedIn won't let a post go over 3,000 characters. We'll build a counter that takes a draft post and tells you three things: how many characters it has, how many words it has, and whether it's over the limit. That's the Scrabble idea at work: count the tiles, then split the row into words.

## Building it
**Step 1: count the tiles and the words.**
```python
post = "Automated my monthly KPI pack. Saved 8 hours a month."

characters = len(post)
words = len(post.split())

print("Characters:", characters)
print("Words:", words)
```
```output
Characters: 53
Words: 10
```
1. `post = "..."` stores your draft in a variable. The quotes mark where the string starts and ends.
2. `len` is one of Python's built-in commands: it counts how many items something has. For a string, that's characters. `len(post)` counts every character, spaces and full stops included. Here that's `53`.
3. `post.split()` cuts the string into separate words wherever there's a space: `"Automated"`, `"my"`, `"monthly"` and so on. Then `len(...)` counts the pieces: `10`.
4. The two `print` lines show `Characters: 53` and `Words: 10`.

**Step 2: check the limit, and tidy the output.** Now we answer "is it too long?" and print the results more neatly.
```python
post = "Automated my monthly KPI pack. Saved 8 hours a month."
characters = len(post)
words = len(post.split())

over_limit = characters > 3000

print(f"Characters: {characters}")
print(f"Words: {words}")
print(f"Over the 3,000 limit? {over_limit}")
```
```output
Characters: 53
Words: 10
Over the 3,000 limit? False
```
1. `characters > 3000` asks a yes or no question: is 53 more than 3000? The answer is a new data type called a **boolean**, which is always either `True` or `False`. Here it's `False`, and we store that in `over_limit`.
2. The `print` lines now use an **f-string**. Put an `f` right before the opening quote, and anything inside `{ }` gets swapped for its value. So `f"Words: {words}"` shows `Words: 10`. It's an easy way to mix text and values in one string.
3. The last line shows `Over the 3,000 limit? False`.

Now paste in a real draft of your own:

[[widget:post-counter]]

## Why this matters
Before you post, you can check a draft in a second instead of guessing. The same three tools, `len`, `split` and f-strings, come up whenever you clean up names in a spreadsheet export or build a message out of pieces of data.

## The mistake beginners make here
Strings must match exactly, character by character. To Python, `"Hello"` and `"hello"` are different strings, because a capital H is a different character from a small h. Even an extra space makes two strings different. In Python, `==` (two equals signs) asks "are these exactly the same?", so `"Hello" == "hello"` gives `False`. When you compare text, like checking a name in a list, make sure the capitals and spaces match too.

## What's next
Next, we'll learn about **lists**: one variable that holds many items in order, like every task on your to-do list.
