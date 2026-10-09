# Lists

## The idea
Think of a to-do list on a notepad. The tasks sit in order, one per line. You can read any line, add a new task at the bottom, or cross off the last one.

In Python, that notepad is called a **list**. A list is one variable that holds many items, in order. You write it with square brackets, and a comma between each item.

## The project: Weekly Task Tracker
We'll keep this week's tasks in a list. Then we'll do the three things you'd do with a real notepad: read a task, add one at the bottom, and remove the last one. The live tool for this lesson has a button for each.

## Building it
```python
tasks = ["Buy milk", "Walk the dog", "Do homework"]

print(tasks[0])

tasks.append("Pay rent")
print(tasks)

tasks.pop()
print(tasks)
```
```output
Buy milk
['Buy milk', 'Walk the dog', 'Do homework', 'Pay rent']
['Buy milk', 'Walk the dog', 'Do homework']
```
Here is what each line does:
1. `tasks = [...]` stores three tasks in one list called `tasks`.
2. `tasks[0]` reads one item by its position. Python counts positions from `0`, not 1. So `tasks[0]` is the first task, `"Buy milk"`, and `tasks[2]` is the third, `"Do homework"`. A position like this is called an **index**.
3. `tasks.append("Pay rent")` adds `"Pay rent"` to the end of the list. Now there are four tasks.
4. `print(tasks)` shows the whole list: `['Buy milk', 'Walk the dog', 'Do homework', 'Pay rent']`.
5. `tasks.pop()` removes the last item, so `"Pay rent"` is gone again.
6. The final `print(tasks)` shows the original three tasks.

The dot in `tasks.append(...)` means "do this to the list called `tasks`". A command attached to a value like this is called a **method**.

[[widget:list-predict]]

## Why this matters
Most real data comes as a list of things: invoices, clients, rows in a report. Once your items sit in one list, you can add to it, remove from it and, from lesson 10, run the same step on every item automatically.

## The mistake beginners make here
The common slip is asking for a position that doesn't exist. Our list has three items, at positions 0, 1 and 2. If you ask for `tasks[3]`, expecting "the third one", Python stops with `IndexError: list index out of range`. Remember: the last position is always one less than the number of items. `len(tasks)` tells you how many items there are.

## What's next
Next, we'll meet two cousins of the list: **tuples**, which can never change, and **sets**, which never hold the same item twice.
