# Handling Errors

## The idea
Think about paying at a shop when your card is declined. The till doesn't shut down and lock the doors. The cashier has a plan for exactly that problem: "card declined, try another one or pay cash". One expected problem, one prepared response, and the shop carries on.

In Python, when something goes wrong while the code is running, it raises an **error** (also called an **exception**), and by default the whole program stops. A **try/except** block is your prepared plan. You put the risky line under `try`, and under `except` you say which error you expect and what to do instead of stopping.

## The project: Safe Cost per Unit Calculator
We'll work out the cost per unit of a purchase: total cost divided by number of units. The risky moment is a units figure of 0, because nothing can be divided by zero. Like the cashier, we'll prepare for that one specific problem and show a clear message instead of crashing.

## Building it
First, see what happens without a plan. Dividing by zero stops the program with a **ZeroDivisionError**, the specific error Python raises whenever something is divided by zero:
`ZeroDivisionError: division by zero`

Now with a plan:
```python
total_cost = 1200
units = 0

try:
    cost_per_unit = total_cost / units
    print(f"Cost per unit: {cost_per_unit}")
except ZeroDivisionError:
    print("Can not work out cost per unit: units is 0.")
```
```output
Can not work out cost per unit: units is 0.
```
Here is what each line does:
1. `total_cost = 1200` and `units = 0` store the purchase figures. Units is 0 on purpose, to trigger the problem.
2. `try:` means "attempt the indented lines below".
3. `cost_per_unit = total_cost / units` is the risky line. Dividing by 0 raises a `ZeroDivisionError`, so Python skips the rest of the `try` block and jumps straight to the matching `except`.
4. `except ZeroDivisionError:` names the one error we prepared for. Its indented line runs only if that exact error happened.
5. The screen shows `Can not work out cost per unit: units is 0.` and the program carries on.

Change `units` to `4` and run it again. Nothing goes wrong, so the `except` part is skipped and you see `Cost per unit: 300.0`.

Step through it and watch the jump. Line 6, the `print` inside `try`, never runs:

[[widget:safe-divide-trace]]

Now try different unit counts:

[[widget:units-calc]]

## Why this matters
Real data is messy: an empty cell, a zero, a supplier file in the wrong format. Without a plan, one bad row stops the whole script. The Excel Formula Generator on this site uses the same idea. If the AI service it calls fails, the tool catches the error and shows you a message instead of a broken page.

## The mistake beginners make here
The common slip is catching everything with a bare `except:` (no error name). It looks safe, but it hides problems you didn't plan for. Say `units` arrives as the text `"4"`. Then `1200 / "4"` raises a `TypeError`, not a division problem, but a bare `except:` would still print "units is 0", which is simply wrong. Name the error you expect, like `except ZeroDivisionError:`, so any other problem still shows up and gets fixed.

## What's next
Next, we'll learn about **reading and writing files**, so your programs can save information and pick it up again next time they run.
