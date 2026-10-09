# What is Code

## The idea
Think of a recipe card. It's a list of steps written down in order. Whoever follows it starts at the top and does one step at a time until the end. They don't skip ahead, and they don't guess what you meant.

A **program** works the same way. It's a list of instructions that a computer follows from the top line to the bottom line, one at a time. The instructions themselves are called **code**.

There's one big difference from a recipe. A person can work out what "a pinch of salt" means. A computer can't. Code has to be written in an exact shape that the computer has been built to understand. In this course, that shape is a language called **Python**.

## The project: Email Signature Generator
We'll write your first program: four instructions that show your email signature on the screen, one line each. It's the recipe card idea in action. The computer will follow your four lines from top to bottom, in order, and when it's done you can copy the result straight into your email.

## Building it
Quick heads up before you read the code: `print` has nothing to do with paper or a printer. In Python, it means "show this text on the screen". That's it.
```python
print("Nabilah Azman")
print("Reporting Analyst, Warner Music Group")
print("nabilah@example.com | +60 12 345 6789")
print("linkedin.com/in/nurnabilahazman")
```
```output
Nabilah Azman
Reporting Analyst, Warner Music Group
nabilah@example.com | +60 12 345 6789
linkedin.com/in/nurnabilahazman
```
Here is what happens when the computer runs this:
1. Line 1 shows `Nabilah Azman` on the screen.
2. Line 2 shows the job title underneath it.
3. Line 3 shows the email and phone number.
4. Line 4 shows the LinkedIn link.

The text inside the quotes is shown exactly as you typed it. The quotes themselves don't appear. They're how you tell Python "this is text to show", as opposed to an instruction.

Step through the program line by line, then test yourself on what would change if the lines swapped places:

[[widget:signature-predict]]

[[widget:signature-trace]]

Swap in your own details and you have a real signature.

## Why this matters
Every tool you'll ever use, from Excel macros to the AI tools on this site, is a list of instructions running top to bottom like this. When something goes wrong, the first question is always the same: which line did the computer reach, and what did it actually do there?

## The mistake beginners make here
The most common slip is writing what you mean instead of what Python expects. `print(Hello)` without quotes fails, because Python thinks `Hello` is the name of something it should already know about, and it doesn't. `show("Hello")` fails too, because `show` isn't a Python instruction. The fix is to copy the exact shape: `print("Hello")`.

## What's next
Next, we'll learn about the **command line**, a plain text window where you type instructions to your computer directly, without clicking.
