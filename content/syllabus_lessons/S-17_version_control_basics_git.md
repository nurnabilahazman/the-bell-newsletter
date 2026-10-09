# Version Control Basics

## The idea
Think of a spreadsheet you've saved as `budget_v1.xlsx`, `budget_v2.xlsx`, `budget_final.xlsx` and `budget_final_REAL.xlsx`. You keep copies so you can go back if something breaks. It works, but it's messy, and you can never remember what changed between versions.

**Version control** does the same job properly. It's a system that keeps a saved history of your project, with a note on each save saying what changed. The most popular version control tool is called **git**. Each saved snapshot in git is called a **commit**, and the folder git is tracking is called a **repository**, or **repo** for short.

## The project: Turn the Excel Formula Generator into a git repo
The Excel Formula Generator, this site's first tool, currently lives in a folder with no history. One bad edit and the working version is gone. We'll turn that folder into a git repository and make its first commit: a snapshot of the working version, labelled so you can always get back to it.

## Building it
**One time setup.** Git labels every commit with your name and email. Tell it once, in the terminal:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Every project.** In the terminal, `cd` into the project folder, then:
```bash
git init
git status
git add formula_generator.py
git commit -m "First working version"
git log --oneline
```
Here is what each command does:
1. `git init` turns the current folder into a repository. Git starts watching it, but hasn't saved anything yet.
2. `git status` shows what git sees. Right now it lists `formula_generator.py` as "untracked": git knows the file is there, but it isn't in any snapshot.
3. `git add formula_generator.py` picks this file to go into the next snapshot. This is called **staging**. To pick every file in the folder at once, use `git add .`
4. `git commit -m "First working version"` takes the snapshot of everything you staged. The text after `-m` is the note, saying what this version is.
5. `git log --oneline` lists your commits, newest first, each with a short code and its note.

Now, if a later edit breaks the file, `git restore formula_generator.py` (restore means "bring back") puts it back exactly as it was in your last commit, throwing away any changes since.

Here is that whole sequence run for real, followed by a bad edit and a restore:

[[widget:git-session]]

[[widget:restore-predict]]

## Why this matters
You can experiment freely. Try a new feature, and if it goes wrong, go back to the last commit in one command. The history also tells you what changed and when, which matters as soon as a project gets bigger than one file.

## The mistake beginners make here
The common slip is working for hours without committing. Git can only bring back what you've committed. Say you make five good changes, then one bad one, without committing in between. `git restore` takes you all the way back to the last commit, and the five good changes are lost too. Commit every time something works, with a short note saying what you did.

Remember that commits live in the `.git` folder on your own computer. If the laptop itself is lost, so are they. That's what the next lesson fixes.

## What's next
Next, we'll learn about **GitHub**: how to send your commits to an online copy, so your work survives even if your laptop doesn't.
