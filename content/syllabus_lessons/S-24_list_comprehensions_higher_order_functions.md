# List Comprehensions and Higher-Order Functions

## The idea
Think of filling down a formula in Excel. You write `=A1*2` once in column B, drag it down, and every row gets its own doubled value in a new column. Column A stays exactly as it was.

A **list comprehension** is Python's fill down. It builds a new list by applying the same step to every item in an existing list, in a single line. The original list is left untouched, just like column A.

## The project: Refactor the LinkedIn Post Character Counter
In lesson 5 our counter split a post into words and counted them. Now we'll get more out of those words in a few short lines: the length of every word, the list of long words, and the single longest word. It's the fill down idea applied to the words of a post.

## Building it
**Step 1: the fill down, on numbers.**
```python
numbers = [1, 2, 3, 4, 5]

doubled_numbers = [x * 2 for x in numbers]

print(doubled_numbers)
print(numbers)
```
```output
[2, 4, 6, 8, 10]
[1, 2, 3, 4, 5]
```
1. `[x * 2 for x in numbers]` reads as "for each `x` in `numbers`, give me `x * 2`, and collect the results in a new list". It's the same job as the loop from lesson 10, written in one line.
2. `doubled_numbers` holds the new list: `[2, 4, 6, 8, 10]`.
3. `print(numbers)` shows `[1, 2, 3, 4, 5]`. The original is unchanged, just like column A.

Here is the fill down happening one item at a time, with your own numbers:

[[widget:comprehension-steps]]

**Step 2: the same idea, on a LinkedIn post.**
```python
post = "Automated my monthly KPI pack and saved 8 hours every month"
words = post.split()

word_lengths = [len(word) for word in words]
long_words = [word for word in words if len(word) > 6]
longest = max(words, key=len)

print(word_lengths)
print(long_words)
print(longest)
```
```output
[9, 2, 7, 3, 4, 3, 5, 1, 5, 5, 5]
['Automated', 'monthly']
Automated
```
1. `words = post.split()` splits the post into words, exactly like lesson 5.
2. `word_lengths = [len(word) for word in words]` makes a new list holding each word's length: `[9, 2, 7, 3, ...]`.
3. `long_words = [word for word in words if len(word) > 6]` adds a filter. The `if` at the end keeps only words longer than 6 letters, giving `['Automated', 'monthly']`. Like filtering a column in Excel before copying it.
4. `longest = max(words, key=len)` finds the longest word and stores it in `longest`. Here's the new idea: we hand the function `len` itself to `max`, without brackets, so `max` can use it to measure each word. A function that takes another function like this is called a **higher-order function**. The answer is `Automated`.

## Why this matters
Cleaning and reshaping lists is everyday work: trimming every name in an export, keeping only invoices over a certain amount, converting every amount to a number. Comprehensions do each of those in one readable line, and functions like `max`, `min` and `sorted` with `key=` answer "which one is the biggest?" questions without a loop.

## The mistake beginners make here
The common slip is expecting the comprehension to change the original list. It never does. It builds a brand new list, and if you don't store that list in a variable, it's simply thrown away. Writing `[x * 2 for x in numbers]` on its own line changes nothing. Always assign it, like `doubled_numbers = [x * 2 for x in numbers]`, and use the new name from then on.

[[widget:store-compare]]

## What's next
Next, we'll learn about **dates and text patterns**: how to check whether a date is in the past, and whether an email address looks valid.
