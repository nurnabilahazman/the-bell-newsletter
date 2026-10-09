# Why Speed Matters

## The idea
Picture two ways of finding a colleague's post in the office mailroom. In the first, all the letters sit in one big pile, and you check them one at a time until you find the right name. In the second, every person has their own labelled pigeonhole, so you walk straight to "Emma" and take what's there.

With 5 letters, both ways are quick. With 5,000 letters, the pile takes ages, while the pigeonhole is just as fast as before. In code, checking items one at a time is called a **linear search**. Going straight to the right spot by its label is what a **dictionary** does, the same type you met in lesson 8.

## The project: Compare two ways of searching the Contact Book
We'll search our contact book for "Emma" in both ways. For the pile, we'll count the **steps**: how many names Python has to look at. The pigeonhole needs no counting, because it goes straight to Emma's key. Counting steps is more useful than timing with a stopwatch. A stopwatch gives a different answer every run, while the step count stays the same and shows what happens as the data grows.

## Building it
**Way 1: the pile. Check every name until you find Emma.**
```python
names = ["Alice", "Bob", "Charlie", "David", "Emma"]
target = "Emma"

steps = 0
for name in names:
    steps = steps + 1
    if name == target:
        break

print(f"One by one: found {target} after {steps} steps")
```
```output
One by one: found Emma after 5 steps
```
Here is what each line does:
1. `names` is a list of five names, and `target` is the name we're looking for.
2. `steps = 0` starts a counter at zero.
3. `for name in names:` is the loop from lesson 10. It looks at one name at a time.
4. `steps = steps + 1` adds one to the counter for every name we look at.
5. `if name == target:` checks whether this is Emma. When it is, `break` stops the loop early, because there's no need to keep looking.
6. The `print` shows `One by one: found Emma after 5 steps`. Emma was last in the pile, so we checked all five.

**Way 2: the pigeonholes. Look Emma up by her key.**
```python
contact_book = {"Alice": "011", "Bob": "012", "Charlie": "013", "David": "014", "Emma": "015"}
target = "Emma"

print(f"Dictionary: {contact_book[target]}, found by its key in one step")
```
```output
Dictionary: 015, found by its key in one step
```
`contact_book[target]` goes straight to Emma's entry without looking at anyone else. Behind the scenes, Python uses the key itself to work out where the value is stored, just like reading the label on a pigeonhole. That's why a dictionary lookup takes about the same time whether it holds 5 names or 5 million.

Before you try the sizes below, make a prediction:

[[widget:steps-predict]]

## Why this matters
At 5 names you'll never notice the difference. At 50,000 rows of transactions, a one by one search for every lookup can turn a one second job into a coffee break. Picking the right type, a dictionary for "find by name", is often the simplest way to make a slow script fast.

## The mistake beginners make here
The common slip is testing with a tiny list, seeing it's fast, and assuming it will stay fast. A linear search gets slower in step with the data: twice as many names can mean twice as many steps. If you're going to look things up by a name or an ID again and again, store them in a dictionary instead of a list.

## What's next
Next, we'll learn about **modules and imports**: how to borrow ready made code that ships with Python, instead of writing everything yourself.
