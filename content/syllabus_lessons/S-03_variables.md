# Variables

## The idea
Think of a row of labelled boxes on a shelf. One label says "name", another says "title". You put something in each box once. After that, whenever you need it, you just ask for the box by its label instead of writing the thing out again.

In code, that labelled box is called a **variable**. A variable is a name that holds a value, so your program can use that value later just by mentioning the name.

## The project: Digital Business Card Generator
We'll store three things about you in three labelled boxes: your name, your job title and your company. Then we'll print a business card by asking for each box by its label. Change what's in a box, and the card changes everywhere that box is used.

## Building it
```python
name = "Nabilah Azman"
title = "Reporting Analyst"
company = "Warner Music Group"

print("Name:", name)
print("Title:", title)
print("Company:", company)
```
```output
Name: Nabilah Azman
Title: Reporting Analyst
Company: Warner Music Group
```
Here is what each line does:
1. `name = "Nabilah Azman"` puts the text `Nabilah Azman` into a box labelled `name`. The `=` sign here doesn't mean "equals" like in maths. It means "store this value under this name".
2. `title = "Reporting Analyst"` stores the job title in a box labelled `title`.
3. `company = "Warner Music Group"` stores the company in a box labelled `company`.
4. `print("Name:", name)` shows the text `Name:` followed by whatever is in the `name` box. The comma tells `print` to show both things side by side with a space between them. So the screen shows `Name: Nabilah Azman`.
5. The last two lines do the same for `title` and `company`.

Notice the difference between `"name"` with quotes and `name` without. With quotes, it's just the text "name". Without quotes, Python opens the box called `name` and uses what's inside.

Step through it and watch each box fill up before it's used:

[[widget:card-trace]]

[[widget:quotes-predict]]

## Why this matters
If your job title changes, you edit one line, and every place that uses `title` picks up the new value. That's the same reason you put a tax rate in one Excel cell and point every formula at it, instead of typing 0.06 into fifty formulas.

## The mistake beginners make here
The most common slip is asking for a box before anything was put in it. If you write `print(phone)` without ever writing a line like `phone = "012 345 6789"` first, Python stops with `NameError: name 'phone' is not defined`. Python runs top to bottom, so the line that stores a value must come before any line that uses it.

## What's next
Next, we'll learn about **operators and data types**: how to do maths with your variables, and why Python treats numbers and text differently.
