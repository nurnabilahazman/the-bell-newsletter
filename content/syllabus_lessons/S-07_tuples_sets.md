# Tuples and Sets

## The idea
Think about two kinds of list you keep at work. The first is a printed menu from your favourite lunch place. It's laminated: you can read it, but you can't scribble on it. The second is a guest list at the door of an event. Nobody gets written down twice, however many times they turn up.

Python has a type for each:
1. A **tuple** is like the laminated menu. It holds items in order, and once it's made, it can never be changed. You write it with round brackets.
2. A **set** is like the guest list. It holds each item only once, and quietly ignores repeats. You can make one from a list with `set(...)`.

## The project: Duplicate Email Remover
Newsletter sign-up lists get messy. The same person signs up twice, and then gets every email twice. We'll use the guest list idea, a set, to remove the repeats. Then we'll see why a tuple is the right home for things that should never change.

## Building it
**Step 1: remove the duplicates with a set.**
```python
email_list = ["john@example.com", "jane@example.com", "john@example.com", "bob@example.com"]

unique_emails = set(email_list)

print(len(email_list))
print(len(unique_emails))
print(sorted(unique_emails))
```
```output
4
3
['bob@example.com', 'jane@example.com', 'john@example.com']
```
Here is what each line does:
1. `email_list` is an ordinary list with four emails. John signed up twice.
2. `set(email_list)` builds a set from the list. Because a set holds each item only once, the second John disappears.
3. `len`, from lesson 5, counts the items. The two `len` lines show `4`, then `3`: one duplicate removed.
4. `sorted` is a built-in command that arranges items in order. `sorted(unique_emails)` gives you a new list with the three emails in alphabetical order, and `print` shows it.

Why sort them? A set only promises "no repeats", not "same order". If you print the set itself, with `print(unique_emails)`, Python shows the emails inside curly brackets in an order that can change every time you run the program. Sorting gives you the same, readable order every run.

[[widget:dedupe]]

**Step 2: a tuple for things that must not change.**
```python
menu = ("pizza", "sushi", "tacos")

print(menu[0])
```
`menu[0]` reads the first item, `"pizza"`, using a position number just like a list. What you can't do is change it. That's the point: a tuple protects values that should stay fixed.

## Why this matters
Duplicates cause real problems: a client emailed twice, an invoice counted twice in a total. Turning a list into a set is the quickest way to find out how many unique items you really have. Tuples are useful for values that should never be edited by accident, like a fixed list of departments.

## The mistake beginners make here
The common slip is treating a tuple like a list and trying to change it. `menu[0] = "burger"` stops with `TypeError: 'tuple' object does not support item assignment`. If you need to add, remove or change items, use a list. Use a tuple only when the values should stay fixed.

## What's next
Next, we'll learn about **dictionaries**, which store information in pairs, like a contact book that matches each name to a phone number.
