# Dictionaries

## The idea
Think of the contacts app on your phone. You don't scroll through every number to find your manager. You search their name, and the number comes up. Each entry is a pair: a name and the number that goes with it.

In Python, this is called a **dictionary**. A dictionary stores information in pairs. The part you look up by is called the **key** (the name). The information it leads to is called the **value** (the phone number). Each key appears only once.

## The project: Client Contact Book
We'll build a small client contact book that does the four things your phone's contacts app does: add a contact, look one up, update a number, and delete a contact. Every one of those is a single line of Python on a dictionary.

## Building it
**Step 1: add a contact, then look it up.**
```python
contact_book = {}

contact_book["John Doe"] = "012-345-6789"
print(contact_book["John Doe"])
```
```output
012-345-6789
```
1. `contact_book = {}` creates an empty dictionary. Curly brackets with nothing inside mean "no pairs yet".
2. `contact_book["John Doe"] = "012-345-6789"` adds a pair. `"John Doe"` is the key, the phone number is the value.
3. `print(contact_book["John Doe"])` looks up the key and shows its value: `012-345-6789`. This is the "search by name" step.

**Step 2: update the number, then delete the contact.** Here is the full program, with four new lines at the bottom:
```python
contact_book = {}
contact_book["John Doe"] = "012-345-6789"

contact_book["John Doe"] = "098-765-4321"
print(contact_book)

del contact_book["John Doe"]
print(contact_book)
```
```output
{'John Doe': '098-765-4321'}
{}
```
1. `contact_book["John Doe"] = "098-765-4321"` uses the same key again. Because each key appears only once, this replaces the old number instead of adding a second John.
2. `print(contact_book)` shows the whole dictionary: `{'John Doe': '098-765-4321'}`.
3. `del contact_book["John Doe"]` deletes that pair. `del` is Python's delete command: it removes the key and its value together. The last `print` shows `{}`: the book is empty again.

Look up a name yourself, the risky way and the safe way:

[[widget:dict-lookup]]

## Why this matters
Lots of work data is pairs: client name and email, invoice number and amount, product code and price. A dictionary finds the right value straight from the key, so you never search line by line. It's the Python version of a VLOOKUP.

## The mistake beginners make here
The common slip is looking up a key that was never added. `contact_book["Jane Doe"]` stops with `KeyError: 'Jane Doe'`. Remember that keys must match exactly, capitals and spaces included. If you're not sure a key exists, use the `.get()` method instead. It looks the key up safely: `contact_book.get("Jane Doe", "Not found")` gives back the fallback `"Not found"` rather than an error.

## What's next
Next, we'll learn about **conditionals**, which let your code make decisions, like "if the salary is over 5000, give it more points".
