# Basic Operators and Data Types

## The idea
Think of a calculator. You key in numbers and press `+`, `-`, `×` or `÷` to work things out. Now imagine typing the word "eight" into it. It can't do anything with that, because it's a word, not a number.

Python is the same. The symbols that do maths are called **operators**. And every value in Python has a **data type**, which is simply what kind of value it is. The type decides what you're allowed to do with it. The three types you'll meet first:

1. **int**, short for integer: a whole number, like `50` or `8`.
2. **float**: a number with a decimal point, like `0.1` or `360.0`.
3. **str**, short for string: text, always written inside quotes, like `"Rent"` or `"8"`.

## The project: Freelance Day-Rate Calculator
We'll work out what a freelancer actually takes home for a day: hours worked times the hourly rate, minus a 10% deduction. It's exactly the calculator idea, using Python's operators on numbers stored in variables.

## Building it
**Step 1: the day's pay before deductions.**
```python
hourly_rate = 50
hours_worked = 8

total_cost = hourly_rate * hours_worked
print("Before deduction:", total_cost)
```
```output
Before deduction: 400
```
1. `hourly_rate = 50` and `hours_worked = 8` store two whole numbers (ints) in variables.
2. `total_cost = hourly_rate * hours_worked` multiplies them. In Python, `*` means multiply. The result, `400`, is stored in `total_cost`.
3. `print(...)` shows `Before deduction: 400`.

**Step 2: take off the 10% deduction.** Here is the full program, with three new lines at the bottom:
```python
hourly_rate = 50
hours_worked = 8
total_cost = hourly_rate * hours_worked

deduction = total_cost * 0.1
final_cost = total_cost - deduction
print("The final cost is:", final_cost)
```
```output
The final cost is: 360.0
```
1. `deduction = total_cost * 0.1` works out 10% of 400, which is `40.0`.
2. `final_cost = total_cost - deduction` subtracts, giving `360.0`.
3. `print(...)` shows `The final cost is: 360.0`.

Why `360.0` and not `360`? Because `0.1` is a float. As soon as a float joins a calculation, the answer is a float too, so Python shows the `.0`. The value is still exactly 360. The four maths operators are `+` add, `-` subtract, `*` multiply and `/` divide. Note that `/` always gives a float: `50 / 10` is `5.0`.

Change the rate or the hours and watch every step of the calculation update, with the data type of each result:

[[widget:day-rate-substitution]]

## Why this matters
Every money calculation you automate, from a day rate to a VAT figure to a monthly total, is operators acting on numbers. Knowing the data type tells you what the result will look like and whether the calculation will work at all.

## The mistake beginners make here
The classic slip is mixing a number and text with `+`. If someone types their hours as `"8"` (with quotes, so it's text), then `50 + "8"` stops with `TypeError: unsupported operand type(s) for +: 'int' and 'str'`. A **TypeError** is Python's way of saying "these two types can't be used together like this". Python refuses to guess whether you meant maths or joining words. The fix is to keep numbers as numbers: write `8`, not `"8"`.

One surprise: `*` does work between text and a whole number. `"8" * 3` gives `"888"`, the text repeated three times. No error, just not the maths you expected.

## What's next
Next, we'll look closely at **strings**, the text type, and what you can do with them, like counting the characters in a LinkedIn post.
