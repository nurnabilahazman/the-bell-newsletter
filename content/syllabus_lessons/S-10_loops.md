# Loops

## The idea
Imagine you need to number 500 invoices for a small business. The first is 1001, the next is 1002, then 1003. Each time, you do the same thing: use the next number.

`1001 → 1002 → 1003 → 1004 → 1005 → …`

You could type all 500 numbers yourself. But it's the same small step, repeated 500 times. A **loop** lets you write that step once and ask Python to repeat it for you. We'll start with just five numbers, so you can see exactly what happens at every step.

## The project: Batch Invoice Number Generator
You give the program a starting number and a quantity. It prints that many invoice numbers, in order, one per line. With a start of `1001` and a quantity of `5`, the exact output is:
```output
Invoice Number: 1001
Invoice Number: 1002
Invoice Number: 1003
Invoice Number: 1004
Invoice Number: 1005
```
The first number is 1001, the last is 1005, and there are 5 lines. One thing to be clear about: this program prints numbers on the screen. It doesn't create invoice documents, save files or send anything. It's the numbering step only.

## Building it
**Step 1: five numbers, written out.**
```python
for number in range(1001, 1006):
    print(f"Invoice Number: {number}")
```
Here is what each part means, in this exact code:
1. `range(1001, 1006)` produces a run of whole numbers. It starts at 1001 and stops just before 1006, so it gives 1001, 1002, 1003, 1004 and 1005. The second number, 1006, is the **stop**, and the stop is never included.
2. `for number in ...:` is the loop. It means "for each value range gives you, call it `number`, then do the indented line". `for` is how Python spells "for each", and `number` is just a name we chose.
3. The colon at the end of the `for` line says "the steps to repeat come next".
4. `print(...)` is pushed in with 4 spaces. That indent is how Python knows the line belongs inside the loop, so it runs once per value.
5. `f"Invoice Number: {number}"` is an f-string, from the Strings lesson. The `f` before the quotes means `{number}` is replaced with its current value: 1001 the first time, 1002 the next, and so on.

[[widget:loop-predict]]

Now watch it run. Each pass through the loop is called an **iteration**, which just means "one round". Python goes back to the `for` line, takes the next value, runs the indented line, and repeats until range has nothing left.

[[widget:loop-trace]]

**Step 2: make it flexible.** That worked for five numbers. But what if you need 10 tomorrow, or 500 next week? Instead of rewriting the range by hand, store the starting number and the quantity in variables:
```python
start = 1001
count = 5

for number in range(start, start + count):
    print(f"Invoice Number: {number}")
```
```output
Invoice Number: 1001
Invoice Number: 1002
Invoice Number: 1003
Invoice Number: 1004
Invoice Number: 1005
```
The only new part is `range(start, start + count)`. Here it is with the real numbers swapped in:
1. `start + count` is `1001 + 5`, which is `1006`.
2. So `range(start, start + count)` is `range(1001, 1006)`, exactly the range from Step 1.
3. The first number printed is the start: 1001.
4. The stop, 1006, is never printed. The last number printed is one less: `start + count - 1`, which is `1001 + 5 - 1 = 1005`.
5. The total printed is always `count`: 5.

Change the numbers below and watch each line update.

[[widget:range-substitution]]

**Step 3: scale up to 500.** Change one line, `count = 500`, and nothing else:
```python
start = 1001
count = 500

for number in range(start, start + count):
    print(f"Invoice Number: {number}")
```
Now `start + count` is `1001 + 500 = 1501`, so the loop runs over `range(1001, 1501)`. That gives 500 numbers, from 1001 up to 1500. The full output is 500 lines. These are its first three lines:
```output-head
Invoice Number: 1001
Invoice Number: 1002
Invoice Number: 1003
```
And these are its last two lines:
```output-tail
Invoice Number: 1499
Invoice Number: 1500
```
Same three lines of loop, now doing 100 times the work. Try your own numbers here:

[[widget:invoice-generator]]

[[widget:range-explorer]]

:::details Bonus: what if the numbers already exist?
A loop doesn't need range. It can also go through a list you already have, like the lists from lesson 6:
```python
invoice_numbers = [1001, 1002, 1003]

for number in invoice_numbers:
    print(f"Invoice Number: {number}")
```
```output
Invoice Number: 1001
Invoice Number: 1002
Invoice Number: 1003
```
Here `invoice_numbers` is a list holding three numbers that already exist, and the loop visits each one in turn. A list holds values you already have. `range()` makes a run of numbers for you. A `for` loop can go through either one, one item at a time.
:::

## Why this matters
Any time you'd do the same step for every row, file or client, a loop can do it for you. Generating reference numbers, going through every row of a report, or checking every item in a list are all loops. On its own, this loop only prints numbers. Creating invoice files, updating a database or sending emails would each need extra code inside the loop.

## The mistake beginners make here
The most common slip is the stop number. To print five invoice numbers from 1001, it feels natural to write `range(1001, 1005)`, because 1005 is the last number you want. But the stop is never included, so you get only four: 1001 to 1004. Python shows no error. You just quietly end up one short.

[[widget:range-mistake]]

The habit that prevents it: write the stop as `start + count`. Then the number of values always equals `count`.

:::details Troubleshooting: an empty list versus a list that doesn't exist
These two look similar, but behave very differently.

An empty list exists. It just has nothing in it, so the loop runs zero times. There's no output and no error:
```python
invoice_numbers = []

for number in invoice_numbers:
    print(number)
```

A list that was never created is different. Python stops with an error, because there's nothing called `undefined_list` at all:
```python expect-error=NameError
for number in undefined_list:
    print(number)
```
```output
NameError: name 'undefined_list' is not defined
```
If you see this error, check the spelling of the name, and check that the line creating the list runs before the loop.
:::

## What's next
Our loop works. But what if you want to reuse it tomorrow, with a different start and count, without copying it again? Next lesson, **functions** let you give these lines a name, like `make_invoices`, and run them whenever you need.
