# Reading and Writing Files

## The idea
Think of an expense notebook. Every time you spend money, you open it, write a new line at the bottom, and close it. Next week, the old lines are still there, so you can add them all up for a running total.

A Python program, on its own, forgets everything the moment it finishes. A **file** is how it gets a notebook: a place on your computer where information stays after the program ends. **Writing** puts information into a file. **Reading** gets it back out.

## The project: Expense Log
We'll build an expense log that remembers. Every time it runs, it adds a new expense to the bottom of a file called `expenses.txt`, then reads every line back and adds up the running total. Run it twice and the total grows, because the notebook kept the first entry.

## Building it
```python
with open("expenses.txt", "a") as file:
    file.write("Rent,1000\n")

total = 0
with open("expenses.txt", "r") as file:
    for line in file:
        parts = line.split(",")
        total = total + float(parts[1])

print(f"Running total: {total}")
```
```output
Running total: 1000.0
```
Here is what each line does:
1. `open("expenses.txt", "a")` opens the file. The `"a"` means **append**: add to the end and keep everything already there. If the file doesn't exist yet, Python creates it.
2. `with ... as file:` gives the open file the name `file` for the indented lines below, and closes it automatically when they finish. Closing is what makes sure your writing is actually saved.
3. `file.write("Rent,1000\n")` writes one line: the item, a comma, the amount. The `\n` means "new line", so the next entry starts on a fresh line.
4. `total = 0` starts the running total.
5. `open("expenses.txt", "r")` opens the same file again, this time in **read** mode, `"r"`.
6. `for line in file:` is a loop that hands you the file one line at a time.
7. `line.split(",")` cuts `"Rent,1000"` at the comma into `["Rent", "1000\n"]`, so `parts[1]` is the amount.
8. `float(parts[1])` turns the text `"1000\n"` into the number `1000.0`, so it can be added to `total`.
9. The `print` shows the total. The first run shows `Running total: 1000.0`. Run it again and you get `2000.0`, because the file now holds two lines.

[[widget:second-run-predict]]

Run the program as many times as you like, in either mode, and watch what happens to the file:

[[widget:file-sim]]

## Why this matters
Anything you want to keep between runs, an expense log, a list of clients, settings, has to live in a file (or a database, later on). Reading a file line by line is also how you'd process a CSV export from your bank or your accounting system.

## The mistake beginners make here
The costly slip is opening with `"w"` when you meant `"a"`. `"w"` means **write**, and it empties the file the moment it opens, before writing anything. Use `"w"` in the expense log and every run wipes out all your previous expenses, leaving only the newest one. Use `"a"` to add to a file, `"w"` only when you really want to start it over, and `"r"` to read.

## What's next
Next, we'll learn about **installing packages and virtual environments**: how to add tools that don't come with Python, and keep each project's tools separate.
