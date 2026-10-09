# Secrets and Environment Variables

## The idea
Think of the PIN for your bank card. You'd never write it on the card itself, because anyone who sees the card would see the PIN. You keep the two apart: the card goes in your wallet, the PIN stays in your head.

Code has PINs too. An **API key** is a secret password that lets your code use an online service, like the AI service behind the tools on this site. If you type the key straight into your code and push the code to GitHub, anyone who sees the code sees your key. So we keep them apart: the code goes on GitHub, the key goes in a separate file that never leaves your computer. That file is called a **.env file**, and the values inside it are called **environment variables**.

## The project: All 10 Bell tools
Every AI tool on this site needs a key called `GROQ_API_KEY`, and none of them has it written in the code. Each one reads it from a `.env` file instead. We'll set up exactly that: a `.env` file, a rule that stops git uploading it, and a few lines of Python that read the key.

## Building it
**Step 1: install the package that reads .env files.** In your project folder, with your virtual environment switched on (lesson 16):
```bash
pip install python-dotenv
```

**Step 2: create the .env file.** Make a file called exactly `.env` in your project folder, containing one line:
```bash
GROQ_API_KEY=paste-your-real-key-here
```

**Step 3: tell git never to upload it.** This step is what keeps the secret off GitHub:
```bash
echo ".env" >> .gitignore
```
A `.gitignore` file is a list of files git should pretend aren't there. This command adds `.env` to that list. Now `git add .` skips it, so it can never be committed or pushed. Run `git status` to check: `.env` should not appear. Here is the difference, from a real run:

[[widget:gitignore-compare]]

**Step 4: read the key in Python.**
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if api_key is None:
    print("No GROQ_API_KEY found. Check your .env file.")
else:
    print(f"Key loaded. It starts with {api_key[:4]}...")
```
1. `import os` fetches Python's built in module for talking to your computer's settings.
2. `from dotenv import load_dotenv` fetches one function from the package you installed. Note the names differ: you install `python-dotenv`, but import `dotenv`.
3. `load_dotenv()` reads your `.env` file and loads each line as an environment variable.
4. `os.getenv("GROQ_API_KEY")` gets the value. If there isn't one, you get `None`, Python's word for "nothing".
5. The `if` checks the key loaded. We only print the first 4 characters, `api_key[:4]`, as proof. Never print the whole key: screens get shared and terminal output ends up in screenshots.

## Why this matters
Leaked keys get found fast. People run programs that scan public GitHub code for keys, and a leaked key can run up charges on your account or expose your data. Keeping keys in `.env`, and `.env` in `.gitignore`, is how every professional project, and every tool on this site, handles secrets.

## The mistake beginners make here
The common slip is the shortcut: `api_key = "gsk_abc123..."`, typed straight into the code "just for now". Then the file gets committed and pushed, and the key is public. Deleting the line later doesn't help, because git keeps the history. If a key ever reaches GitHub, treat it as leaked: create a new key on the service's website and delete the old one. Always put secrets in `.env` from the start.

## What's next
Next, we'll learn about **classes**, a way to bundle data and the actions that go with it, like a client and everything you can do with a client record.
