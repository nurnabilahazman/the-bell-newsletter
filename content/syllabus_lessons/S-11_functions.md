# Functions

## The idea
Think of a saved Excel template for a client invoice. You set it up once: where the hours go, where the rate goes, and the formula that multiplies them. After that, for every new client you just fill in their hours and rate, and the total appears. You never rebuild the formula.

In Python, that reusable template is called a **function**. A function is a named block of code you write once and can run again whenever you need it, with different numbers each time.

## The project: Day-Rate Calculator, as a function
In lesson 4 we worked out a day rate with loose lines of code. If you had three clients, you'd copy those lines three times. Instead, we'll wrap the calculation in a function called `day_rate_calculator`, then use it for two different clients, just like filling in the invoice template twice.

## Building it
```python
def day_rate_calculator(hours, rate):
    total = hours * rate
    return total

client_a = day_rate_calculator(8, 50)
client_b = day_rate_calculator(6, 80)

print(client_a)
print(client_b)
```
```output
400
480
```
Here is what each line does:
1. `def day_rate_calculator(hours, rate):` creates the function. `def` is short for "define". `hours` and `rate` are blank slots, like the empty cells in the template. They're called **parameters**.
2. `total = hours * rate` is the formula. It's indented, so it belongs to the function.
3. `return total` hands the answer back to whoever used the function. Without `return`, the function would do the maths but hand back `None`, Python's word for "nothing", so `client_a` would end up empty.
4. `day_rate_calculator(8, 50)` runs the function, filling the slots: `hours` becomes 8 and `rate` becomes 50. Running a function like this is called **calling** it. The answer, `400`, is stored in `client_a`.
5. `day_rate_calculator(6, 80)` calls it again with different numbers, giving `480` for `client_b`.
6. The two `print` lines show `400` and `480`.

Notice that defining the function doesn't run it. Lines 1 to 3 only set up the template. Nothing is calculated until line 5 calls it. Step through it and watch Python jump into the function, work out `total`, and come back with the answer, twice:

[[widget:function-trace]]

Here's the first call with the real numbers swapped in. `day_rate_calculator(8, 50)` puts 8 in `hours` and 50 in `rate`. So `total = 8 * 50 = 400`, and `return` hands 400 back to be stored in `client_a`. Try your own numbers:

[[widget:day-rate-calc]]

**Why `return` and not `print`?** They look similar, because both seem to "give you the answer". They do different jobs. `print` only shows a value on the screen. `return` hands the value back so the rest of your code can use it, store it or add it up. Compare the two versions:

[[widget:print-vs-return]]

## Why this matters
Write the calculation once, and every client uses the same tested logic. If the formula changes, say a new deduction, you fix it in one place instead of hunting through copies. Every tool on this site is built from functions like this one.

## The mistake beginners make here
The common slip is calling a function before Python has read the `def` for it. Python runs top to bottom, so if the line `day_rate_calculator(8, 50)` comes above the `def`, Python stops with `NameError: name 'day_rate_calculator' is not defined`. Keep your `def` blocks at the top of the file, and call them underneath.

## What's next
Next, we'll look at **why speed matters**: how two pieces of code can give the same answer, but one gets much slower as your data grows.
