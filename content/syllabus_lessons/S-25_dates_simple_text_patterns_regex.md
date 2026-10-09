# Dates and Simple Text Patterns

## The idea
Think of an accounts clerk checking a pile of invoices. For each one, they ask two quick questions. Is the due date already behind us? And does the contact email look like a real email address, something, then an @, then a domain like `example.com`? Neither question needs reading the whole invoice. One compares dates; the other checks the *shape* of some text.

Python has a module for each question. **datetime** understands dates, so it can tell which of two dates comes first. **re**, short for **regular expressions**, checks text against a **pattern**: a description of the shape the text should have, like "letters, then @, then a domain".

## The project: Email Format Validator for the Contact Book
We'll build the clerk's two checks for our contact book: is this invoice overdue, and is this client's email address in a valid format? The second check is the main project: it stops typos like a missing @ from getting into the contact book.

## Building it
**Step 1: is the due date in the past?**
```python
from datetime import datetime, date

due_date = datetime.strptime("2026-09-30", "%Y-%m-%d").date()
is_overdue = due_date < date.today()

print(f"Due {due_date}, overdue: {is_overdue}")
```
```output
Due 2026-09-30, overdue: True
```
1. `from datetime import datetime, date` fetches two tools from the `datetime` module.
2. `due_date = datetime.strptime("2026-09-30", "%Y-%m-%d").date()` reads text as a date and stores it in `due_date`. The first part in the brackets is the date as text. The second part describes its layout: `%Y` is the 4 digit year, `%m` the month, `%d` the day, separated by dashes. `.date()` keeps just the date, without a time.
3. `date.today()` is today's date. `<` between two dates means "comes before", so `is_overdue` is `True` if the due date has already passed.
4. The `print` shows something like `Due 2026-09-30, overdue: True`.

**Step 2: does the email have the right shape?**
```python
import re

pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

for email in ["nabilah@example.com", "nabilah@example", "nabilah.example.com"]:
    is_valid = bool(re.fullmatch(pattern, email))
    print(email, is_valid)
```
```output
nabilah@example.com True
nabilah@example False
nabilah.example.com False
```
The pattern reads left to right, in pieces:
1. `[a-zA-Z0-9._%+-]+` means "one or more of these characters": letters, digits, and `. _ % + -`. That's the name part, like `nabilah`. The square brackets list the allowed characters, and the `+` after them means "one or more".
2. `@` means a literal @ sign.
3. `[a-zA-Z0-9.-]+` is the domain name, like `example`.
4. `\.` is a literal full stop. On its own, `.` means "any character" in a pattern, so the backslash says "I mean an actual dot".
5. `[a-zA-Z]{2,}` is the ending, like `com` or `my`: at least 2 letters.
6. The `r` before the quotes marks a "raw" string, so Python leaves the backslash alone for the pattern to use.

The loop checks three emails. `re.fullmatch(pattern, email)` checks whether the *whole* email fits the pattern, and `bool(...)` turns the answer into `True` or `False`, stored in `is_valid`. The output is `True` for `nabilah@example.com`, and `False` for the other two: one has no ending after the domain, the other has no @.

Check your own dates and emails. Each one is tested with exactly the same rules Python uses:

[[widget:due-date]]

[[widget:email-checker]]

## Why this matters
Dates drive half of finance: overdue invoices, payment terms, month end. Patterns catch bad data at the door, a mistyped email, a malformed invoice number, before it spreads into reports and mail merges.

## The mistake beginners make here
The common slip is trusting a pattern to do more than it can. A pattern only checks the *shape* of text. `nabilah@example.com` passes, but that doesn't mean the mailbox exists. Only sending an email proves that. And a pattern only fits the shape it was written for: run a phone number like `012-345 6789` through the email pattern and it's rejected, which is correct. Each kind of data, emails, phone numbers, invoice numbers, needs its own pattern.

## What's next
That's the end of the Spine, the shared foundation. Next, the course branches into four tracks, starting with building real web products: databases, logins and deploying your own app.
