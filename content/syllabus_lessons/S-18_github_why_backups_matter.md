# GitHub and Backups

## The idea
Think of your git history from the last lesson as a filing cabinet in your home office. It's organised and every version is in there. But if the house floods, the cabinet goes with it. A real backup means a copy of the cabinet somewhere else.

**GitHub** is that somewhere else. It's a website that stores an online copy of your git repository. Sending your commits up to it is called **pushing**. Once you've pushed, your history is safe even if your laptop is lost, and you can download it onto any other computer.

## The project: Push the Week 1 repo to GitHub
We'll take the repository you made in lesson 17 and push it to GitHub, so the Excel Formula Generator's history lives in two places: your laptop and an online copy.

## Building it
**Step 1: make an empty repository on GitHub.** Sign in at github.com, click **New repository**, give it a name, and leave "Add a README" unticked so it starts empty. GitHub then shows you its web address, which looks like `https://github.com/your-username/your-repo.git`.

**Step 2: connect and push.** In the terminal, inside your project folder:
```bash
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```
Here is what each command does:
1. `git remote add origin <address>` tells your local repo where its online copy lives. `origin` is just the nickname for that address, the name almost everyone uses.
2. `git branch -M main` names your line of commits `main`, which is what GitHub expects. Older versions of git call it `master`, and pushing `main` would fail with `src refspec main does not match any`. This command makes sure the name matches either way.
3. `git push -u origin main` sends your commits up to GitHub. The `-u` remembers the pairing, so from now on a plain `git push` is enough.

Here is why step 2 matters, from a real run on a repo whose branch was still called `master`:

[[widget:main-compare]]

The first time you push, git asks you to sign in. GitHub doesn't accept your account password here. It needs a **personal access token**, a long code you create on GitHub under Settings, then Developer settings, then Personal access tokens. Paste the token when asked for a password.

**Every time after that:** commit as usual, then run `git push`.

## Why this matters
Laptops get lost, stolen and spilt on. Anything that's only on one machine can disappear in a second. With your work on GitHub, a broken laptop costs you a new laptop, not your project. It also means you can share your code, or open it on another computer.

One warning: anything you push can end up public. Never push a file that contains a password or API key. Lesson 22 shows how to keep secrets out of your code.

## The mistake beginners make here
The common slip is committing regularly but never pushing. Commits feel like saving, but they only exist on your laptop until you push. If the laptop dies, every commit since your last push dies with it. Make `git push` part of the habit: commit, then push.

## What's next
Next, we leave Python for a moment and learn **HTML**, the language that gives every web page its structure.
