# The Command Line

## The idea
Think about walking around an office building. At any moment you are standing in one room. If someone says "pick up the file on the desk", you look at the desk in the room you're in, not a desk on another floor. To work somewhere else, you first walk to that room.

The **command line** works the same way. It's a window where you type short instructions, called **commands**, instead of clicking. A program called the **terminal** reads each command and asks the computer to carry it out. On a Mac you'll find it by searching for "Terminal".

The terminal always has a "room" you're standing in. That's your current **folder**, which on the command line is also called a **directory**. Commands work in that folder unless you tell them otherwise.

## The project: Navigate & Organize Your Own Project Folders
We'll tidy a messy folder called `Week1` using four commands: walk into the folder, look around, make a new folder, and move a file into it. That's the office idea exactly: go to the right room, see what's on the desk, then rearrange it.

## Building it
These commands assume a folder called `Week1` with a file called `file.txt` inside it. The practice terminal below sets that up for you, so nothing on your own computer is touched. Type the four commands one at a time, pressing Enter after each:
```bash
cd Week1
ls
mkdir NewFolder
mv file.txt NewFolder
```
Here is what each one does:
1. `cd Week1` means "change directory". It walks you into the `Week1` folder. From now on, that's your current folder.
2. `ls` means "list". It shows everything inside your current folder, so you can see `file.txt` is there.
3. `mkdir NewFolder` means "make directory". It creates a new, empty folder called `NewFolder` inside `Week1`.
4. `mv file.txt NewFolder` means "move". It takes `file.txt` and puts it inside `NewFolder`.

Why does `cd Week1` come first? Because `mv file.txt NewFolder` looks for `file.txt` in your current folder. If you're still outside `Week1`, there's no `file.txt` where you're standing, and you get an error. You could also skip the walk and give the full route instead, like `mv Week1/file.txt Week1/NewFolder`. Walking in first just keeps every command short.

[[widget:folder-predict]]

## Why this matters
Most developer tools start from the command line. Installing a package, saving your work with git, and running your Python files later in this course all mean typing a command in the right folder. Knowing which folder you're in saves you from the most confusing errors.

## The mistake beginners make here
The classic slip is running a command from the wrong folder. You type `mv file.txt NewFolder` and get `No such file or directory`, even though you can see the file in Finder. The file is fine. You're just standing in a different folder. Run `ls` to check what's around you, then `cd` into the right folder and try again. Here is the same command run from both places, with the real output from a Mac terminal:

[[widget:wrong-folder]]

## What's next
Next, we'll learn about **variables**, which let a program remember a piece of information under a name so it can use it later.
