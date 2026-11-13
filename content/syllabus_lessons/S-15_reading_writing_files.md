# Reading and Writing Files

## The idea
**What if your expense notebook forgot yesterday's spending?**

On Monday you write **Rent: RM1,000**. On Tuesday you add **Food: RM50.50**. Both entries stay in the notebook, even after you close it.

A Python program normally loses the values in its variables when it finishes. A **file** helps it remember. You can save information in a file and read it again next time.

[[widget:expense-story]]

**Python has three ways to open our expense file.** Which one should we choose?

[[widget:file-mode-compare]]

Remember: **"a" adds, "w" starts over, and "r" reads.** These letters are called *file modes*. They tell Python what it can do with an open file.

## The project: Expense Log
We'll build a program that saves every expense in a text file named `expenses.txt`. A `.txt` file is like a simple notebook on your computer.

The program adds `Rent,1000`, reads the saved expenses, and shows the total.

Starting with an **empty file**, the first run shows `Running total: 1000.0`. Run it again, and the total becomes `2000.0` because the file kept the first entry.

## Building it
Here is the real Python program. **Click steps 1 to 8** to highlight the matching line and see what it does. You can also switch between the first and second run without losing your place.

[[widget:file-code-walkthrough]]

:::details Copy the complete Python code and see its output
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
:::

**The main idea:** `open()` opens the file. `"a"` keeps old expenses while adding a new one. `file.write()` adds text. The `\n` starts a new line.

Then `"r"` opens the file for reading. The `for` loop reads one line at a time. `split(",")` separates the expense name from the amount. `parts[1]` picks the second piece, because Python starts counting at zero. `float()` turns that text into a number, and `total` adds the amounts together. Finally, `print()` shows the total.

**What about `with ... as file`?** It gives the opened file a short name and closes it automatically after the indented block. Closing finishes pending buffered writes, although some data can be flushed earlier.

This beginner example expects each expense to look like `item,amount`, such as `Rent,1000`. Incorrectly formatted lines may cause an error.

**PREDICT FIRST:** If the file starts empty and you run the same program twice, what does the second run print?

[[widget:second-run-predict]]

**TRY IT YOURSELF:** Choose `"a"` or `"w"`, enter an expense, and run the program. Watch how the saved file and running total change. Reset starts with an empty pretend file. The simulation uses JavaScript; no file is saved to your device.

[[widget:file-sim]]

## Why this matters
Imagine downloading a bank statement. Python can read the saved rows and add up the amounts. You could also use files to keep a client list or save information for next time.

## The mistake beginners make here
**Using `"w"` instead of `"a"` can erase your expense history.** When Python opens an existing file in `"w"` mode, it clears the old contents right away.

Use `"a"` to add new expenses without deleting the old ones. Use `"w"` only when you really want to replace the contents. Use `"r"` when you want to read the saved information.

## What's next
Next, we'll learn about **installing packages and virtual environments**: how to add tools that don't come with Python, and keep each project's tools separate.
