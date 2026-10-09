# Organizing Code with Classes

## The idea
Think of a new client form your company uses. The blank form is the same for everyone: a box for name, a box for phone, a box for address, and at the bottom, "print this record". Each new client gets their own filled in copy. The form is designed once, then reused for every client.

In Python, the blank form is called a **class**. A class is a design that bundles some data (the boxes) together with the actions that go with it. Each filled in copy is called an **object**. An action that belongs to the class, like "print this record", is called a **method**: a function that lives inside the class.

## The project: Rebuild the Client Contact Book as a class
In lesson 8, a client was just a name and a phone number in a dictionary. Real clients have more details, and things you want to do with them. We'll design a `Client` class, the blank form, then fill in two clients from it and print each one's record.

## Building it
```python
class Client:
    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address

    def display_info(self):
        print(f"Name: {self.name}, Phone: {self.phone}, Address: {self.address}")

client1 = Client("John Doe", "1234567890", "123 Main St")
client2 = Client("Jane Tan", "0198765432", "8 Jalan Ampang")

client1.display_info()
client2.display_info()
```
```output
Name: John Doe, Phone: 1234567890, Address: 123 Main St
Name: Jane Tan, Phone: 0198765432, Address: 8 Jalan Ampang
```
Here is what each line does:
1. `class Client:` starts the design of the blank form, named `Client`. Class names start with a capital letter by convention.
2. `def __init__(self, name, phone, address):` is a special method that runs automatically every time a new client is made. It fills in the form. The name is "init" (short for initialise) with two underscores on each side.
3. `self` means "this particular client". When John is being made, `self` is John; when Jane is being made, `self` is Jane.
4. `self.name = name` writes the name into this client's own box. The same goes for `phone` and `address`. Values stored on an object like this are called **attributes**.
5. `def display_info(self):` is a method, the "print this record" action. It uses `self` to read this client's own boxes.
6. `Client("John Doe", "1234567890", "123 Main St")` makes a new object from the class, which runs `__init__` with these details. The result is stored in `client1`.
7. `client2` is a second, separate object from the same design, with its own details.
8. `client1.display_info()` runs the method for John only, and shows `Name: John Doe, Phone: 1234567890, Address: 123 Main St`. The next line shows Jane's record.

Step through it and watch `self` fill up, box by box, for each client:

[[widget:client-trace]]

## Why this matters
With one design, you can create as many clients as you need, and each one carries its own data plus the actions that make sense for it. Change the form once, say add an email box, and every client gets it. Most bigger programs, including the web framework behind this site, are organised this way.

## The mistake beginners make here
The common slip is forgetting `self` in a method. If you write `def display_info():` with empty brackets, then calling `client1.display_info()` stops with `TypeError: display_info() takes 0 positional arguments but 1 was given`. Python always passes the object itself into a method, so the method needs a slot for it. Make `self` the first thing in the brackets of every method.

[[widget:self-compare]]

## What's next
Next, we'll learn about **list comprehensions**: a short way to build a new list from an old one in a single line.
