# Installing Packages and Virtual Environments

## The idea
Lesson 13's stationery cupboard comes with Python. But some tools aren't in it. For those, you order from an outside supplier. And if you work on several projects, you keep a separate toolbox for each one. That way a tool you order for one project can't replace the version another project relies on.

In Python, a tool from the outside supplier is called a **package**: code that someone else wrote and published online. The program that fetches packages is called **pip**. The separate toolbox for each project is called a **virtual environment**: a private folder of packages that belongs to one project only.

## The project: Newsletter Signup QR Code Generator
We'll make a real QR code that people can scan to open a sign up page. Python can't do that out of the box, so we'll order a package called `qrcode`. Following the toolbox idea, we'll first make a private virtual environment for this project and install the package into it.

## Building it
**Step 1: set up the toolbox and install the package.** Type these in the terminal, inside your project folder, one at a time:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "qrcode[pil]"
```
1. `python3 -m venv .venv` creates a virtual environment in a new folder called `.venv`. This is the empty, private toolbox.
2. `source .venv/bin/activate` switches it on. Your terminal line now starts with `(.venv)`, which tells you that anything you install goes into this toolbox. (On Windows the command is `.venv\Scripts\activate` instead.)
3. `pip install "qrcode[pil]"` downloads the `qrcode` package. The `[pil]` part also installs Pillow, the package `qrcode` needs to save the code as an image. Without it, saving the image fails.

**Step 2: use the package.** Save this as `make_qr.py` in the same folder:
```python
import qrcode

img = qrcode.make("https://the-bell.onrender.com")
img.save("newsletter_qr.png")
print("Saved newsletter_qr.png")
```
1. `import qrcode` fetches the package, exactly like importing a module from lesson 13.
2. `qrcode.make(...)` turns the link into a QR code picture, stored in `img`.
3. `img.save("newsletter_qr.png")` saves the picture as an image file in your folder.
4. Run it with `python make_qr.py` while the toolbox is switched on. Open the image and scan it with your phone camera.

## Why this matters
Packages turn big jobs into a few lines: reading Excel files, calling AI services, making charts. Virtual environments keep each project working: one project can stay on an older version of a package while another uses the newest one.

## The mistake beginners make here
The common slip is forgetting to switch the toolbox on. You open a new terminal window, run `python3 make_qr.py`, and get `ModuleNotFoundError: No module named 'qrcode'`, even though you installed it. The package is fine. It's sitting in the `.venv` toolbox, which isn't switched on in this window. Run `source .venv/bin/activate` again, check for `(.venv)` at the start of the line, then run your script.

[[widget:activate-compare]]

## What's next
Next, we'll learn about **git**, which keeps a saved history of your project so you can always go back to a version that worked.
