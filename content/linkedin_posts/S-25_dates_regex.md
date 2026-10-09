S-25 · Dates & simple text patterns (regex) · The Bell

You've probably let a mistyped email into your contact list.

A pattern built for one shape of text, like an email, correctly rejects anything that doesn't match that exact shape.

Every lesson on my site follows the exact same shape:

✦ Read the idea. 1 minute, plain English, no jargon.
✦ Try it live in the browser. No install, no account.
✦ A 2 question quiz. Confirms it actually landed.
✦ A real project you keep. Not a toy example.

Lesson twenty five, as proof it's real:

pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
print(bool(re.fullmatch(pattern, email)))

Two lines catch an address with no @ or no .com before it reaches your list. It checks the shape, so it won't tell you if the mailbox exists.

25 lessons. Mapped start to finish, so this is the last one, and you'll have gone from zero to a real project 25 times over.

Step 1. Open lesson twenty five: https://the-bell.onrender.com/syllabus/lesson/S-25/
Step 2. Read it. 1 minute.
Step 3. Try it live. 1 minute.
Step 4. Take the quiz. 1 minute.

3 minutes, during the coffee you're already making.

Free. No login.

♻️ Repost this for someone one skill away from their next job.
