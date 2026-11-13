# Reading and Writing Files

## The idea
Imagine you keep a notebook for your expenses.

Today you write **Rent: RM1,000**. Next week you open the notebook again. The rent entry is still there. You can add **Food: RM50.50** and see that you have spent **RM1,050.50** in total.

A Python program normally loses the values in its variables when it finishes. But a **file** can keep information for the next time the program runs.

Think of it this way:
* **Write**: Put a new expense into your notebook.
* **Read**: Open the notebook and look at your saved expenses.

### Three tiny letters, three different actions
Imagine your file already contains `Rent,1000`.

| Mode | What Python does | What happens to Rent? |
| --- | --- | --- |
| `"a"` (append) | Adds a new line at the end. | **Kept.** |
| `"w"` (write) | Empties the file first, then writes. | **Deleted.** |
| `"r"` (read) | Looks at the saved lines without changing them. | **Kept.** |

Remember: **"a" adds, "w" starts over, "r" reads.** In this project, we use `"a"` to save expenses and `"r"` to add them up.

## The project: Expense Log
Let's build a small program that remembers what you spent.

Each time you run it, the program does two jobs:
1. It adds `Rent,1000` to a text file called `expenses.txt`.
2. It opens that file again, reads the amounts, and adds them together.

**Start with no `expenses.txt` file, or an empty one.** The first run shows `1000.0`. Run the program again and it shows `2000.0`, because both entries are saved.

## Building it
Here's the complete Python code. We'll understand it in small pieces below.

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

### Part 1: Save one expense
Look at the first two lines:

* `open("expenses.txt", "a")`: Find the file named `expenses.txt` and open it for adding. If it does not exist, Python creates it. The `"a"` tells Python **not to erase old entries**.
* `with ... as file:`: Call this opened file `file` inside the indented code. Think of `file` as the name of the notebook while it is open. The `with` block closes it automatically when the block ends.
* `file.write("Rent,1000\n")`: Add the text `Rent,1000`. The comma separates the item from its amount. `\n` tells Python to start a **new line**, ready for the next expense.

After the first run, `expenses.txt` looks like this:

```text
Rent,1000
```

### Part 2: Read the saved expenses
Now we want to add up the amounts in our notebook.

* `total = 0`: Start with nothing spent yet.
* `open("expenses.txt", "r")`: Open the same file to **read** it. The `"r"` does not change what's in the file.
* `for line in file:`: Take one saved line at a time. If there are three expenses, this loop goes through three lines.
* `parts = line.split(",")`: Cut the line at the comma. `Rent,1000\n` becomes `["Rent", "1000\n"]`. Think of it as two labelled pieces: the item and the amount.
* `parts[1]`: Pick the **second** piece, which is the amount. Python counts positions starting at `0`.
* `float(parts[1])`: Turn the amount from text into a number. For example, `"1000\n"` becomes `1000.0`.
* `total = total + float(parts[1])`: Add that number to our running total. Repeat for each line.
* `print(f"Running total: {total}")`: Show the final amount on screen. The `f` lets Python put the value of `total` inside the message.

**Why convert the text?** Python reads file contents as text. We use `float()` because numbers can be added, but expense amounts stored as text cannot be added like numbers.

### What changes on the second run?
The program adds another `Rent,1000` line, because we used `"a"`.

```text
Rent,1000
Rent,1000
```

Now Python reads **both** lines: `1000.0 + 1000.0 = 2000.0`.

Closing a file finishes any pending buffered writes. Some writes may already have been sent earlier. That's why we use `with open(...)`: Python closes the file for us even if something goes wrong inside the block.

**One rule for this beginner project:** Write each expense as `item,amount`, like `Rent,1000`. If a line is missing its amount or contains letters where a number should be, this simple version can raise an error.

[[widget:second-run-predict]]

### Try it yourself
You don't need to install Python to experiment here. Try pressing **Run the program** three times with `"a"` selected. Watch the file grow and the total increase.

Then select `"w"` and run it again. Watch the old entries disappear. Use **Reset** when you want to start with an empty pretend file.

This activity runs in JavaScript and imitates Python's file behaviour. It does **not** create a real file on your computer.

[[widget:file-sim]]

## Why this matters
Think about a bank statement or a spreadsheet export. A program can open a saved file, read its rows, and calculate a total.

The same idea helps with expense records, client lists, and saved settings. Files let your program use information from an earlier run.

## The mistake beginners make here
**Be careful with `"w"`.** It does not mean "add one more expense." It means "start over." Opening an existing file with `"w"` clears its contents immediately.

Imagine your file contains `Rent,1000` and `Food,50.5`:
* Open with `"a"` and write `Transport,20`: **all three** entries stay.
* Open with `"w"` and write `Transport,20`: **only the new entry** remains.
* Open with `"r"`: you can read the existing entries, but not write with that read-only file handle.

Use `"a"` when you want to keep the expense history. Use `"w"` only when you intentionally want to replace it.

## What's next
Next, we'll learn about **installing packages and virtual environments**: how to add tools that don't come with Python, and keep each project's tools separate.
