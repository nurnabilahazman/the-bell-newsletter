# Modules and Imports

## The idea
When you need a stapler at work, you don't build one. You go to the stationery cupboard and take one out. The cupboard is already stocked, but nothing comes out until you go and fetch it.

Python comes with a cupboard like that. It's full of ready made code for common jobs, organised into **modules**. A module is a file of code someone else has already written and tested. To use one, you have to fetch it first with the word **import**, usually at the very top of your file.

## The project: Secure Password Generator
We'll build a password generator by fetching two things from the cupboard instead of writing them ourselves. The `string` module gives us every letter, digit and symbol, ready typed out. The `secrets` module picks characters at random, in a way that's safe for passwords. Python's own documentation says to use `secrets`, not the general purpose `random` module, for anything security related.

## Building it
```python
import secrets
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(length):
        password = password + secrets.choice(characters)
    return password

print(generate_password(12))
```
Here is what each line does:
1. `import secrets` and `import string` fetch the two modules. From now on, you can use what's inside them by writing the module name, a dot, and the thing you want.
2. `def generate_password(length):` creates a function, like in lesson 11. `length` is how many characters the password should have.
3. `string.ascii_letters + string.digits + string.punctuation` joins three ready made strings: all letters a to z and A to Z, the digits 0 to 9, and symbols like `!` and `?`. That's 94 characters to choose from, stored in `characters`.
4. `password = ""` starts with an empty string, two quotes with nothing between them.
5. `for i in range(length):` repeats the next line `length` times, 12 here. We don't need `i` itself; we just want 12 rounds.
6. `secrets.choice(characters)` picks one random character, and `password = password + ...` adds it to the end. After 12 rounds, the password is 12 characters long.
7. `return password` hands it back, and `print(...)` shows it. You'll get something different every time, like `FX[l|%kphpJf`. That's why this lesson can't show you "the" output: a random password is a different 12 characters on every run, which is exactly what you want.

[[widget:random-predict]]

## Why this matters
Modules save you from rebuilding tools that already exist and have been tested by thousands of people. In finance work, `csv` reads a bank or accounting export, `datetime` handles due dates and month ends, and `statistics` works out averages and medians. All three are already in the cupboard. Python ships with modules for dates, files, maths, randomness and much more. Knowing to look in the cupboard first is half of being productive in code.

## The mistake beginners make here
The common slip is using something from a module without importing it first. If you delete `import secrets`, Python stops at `secrets.choice` with `NameError: name 'secrets' is not defined`. It has no idea where `secrets` is until you fetch it. Keep all your `import` lines at the top of the file, so they run before anything uses them.

[[widget:missing-import]]

## What's next
Next, we'll learn about **handling errors**: how to tell Python what to do when something goes wrong, instead of letting the whole program stop.
