# Conditionals

## The idea
Think about how you decide on a job offer. If the salary is high enough, it gets a big tick. Otherwise, it gets a smaller one. And if the office is in KL, that's a bonus on top. Each decision is a question with a yes or no answer, and what you do next depends on the answer.

In code, this is called a **conditional**. A conditional checks whether something is true, then runs one set of instructions if it is, and a different set (or nothing) if it isn't. Python spells it `if` and `else`.

## The project: Mini Job Offer Scorer
We'll turn those two decisions into code. A salary over 5000 scores 10 points, anything else scores 5. An office in KL adds 2 bonus points. It's a hand built version of the "Should I Take This Job?" tool on this site, minus the AI.

## Building it
```python
salary = 6000
location = "KL"

if salary > 5000:
    score = 10
else:
    score = 5

if location == "KL":
    score = score + 2

print(score)
```
```output
12
```
Here is what each line does:
1. `salary = 6000` and `location = "KL"` store the offer's details.
2. `if salary > 5000:` asks "is the salary more than 5000?". The answer is `True` or `False`, just like the booleans from the Strings lesson. The colon at the end means "here comes what to do".
3. `score = 10` is pushed in with 4 spaces. That indent is how Python knows this line belongs to the `if`. It only runs when the answer is `True`.
4. `else:` means "otherwise". The indented `score = 5` under it only runs when the answer was `False`.
5. `if location == "KL":` asks "is the location exactly KL?". Remember, `==` compares, while a single `=` stores.
6. `score = score + 2` takes the current score, adds 2, and stores the result back in `score`. You'll often see the shortcut `score += 2`, which means exactly the same thing.
7. `print(score)` shows `12`: 10 for the salary, plus 2 for KL.

Step through it and watch each check come out True or False:

[[widget:scorer-trace]]

Then score your own offer. Try a salary of exactly 5000, and try typing kl in lowercase:

[[widget:scorer-calc]]

## Why this matters
Every rule you apply at work can be written this way. If the invoice is over 30 days old, flag it. If the expense is over the limit, send it for approval. Once a rule is in code, it gets applied the same way every time.

## The mistake beginners make here
The common slip is the boundary. What happens with a salary of exactly 5000? `5000 > 5000` is `False`, because 5000 isn't more than itself. So the offer drops into the `else` and scores 5, not 10. Python handles it fine; it just might not be what you meant. If 5000 should count as high enough, write `salary >= 5000`, which means "more than or equal to". Always test the exact boundary value before trusting a rule.

## What's next
Next, we'll learn about **loops**, which repeat the same step for every item in a list, like stamping a number on every invoice in a book.
