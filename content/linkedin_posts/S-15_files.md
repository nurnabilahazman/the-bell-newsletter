S-15 · Reading & writing files · The Bell

One letter can wipe out a month of expenses.

Open a file in the wrong mode and Python empties it before writing a single line.

Every lesson on my site follows the exact same shape:

✦ Read the idea. 1 minute, plain English, no jargon.
✦ Try it live in the browser. No install, no account.
✦ A 2 question quiz. Confirms it actually landed.
✦ A real project you keep. Not a toy example.

Lesson fifteen, as proof it's real:

with open("expenses.txt", "a") as file:
    file.write("Rent,1000\n")

"a" adds to the end and keeps every expense you logged before. "w" would wipe them all, every single run.

25 lessons. Mapped start to finish, so you always know what's next and nothing gets skipped.

Step 1. Open lesson fifteen: https://the-bell.onrender.com/syllabus/lesson/S-15/
Step 2. Read it. 1 minute.
Step 3. Try it live. 1 minute.
Step 4. Take the quiz. 1 minute.

3 minutes, during the coffee you're already making.

Free. No login.

♻️ Repost this for someone one skill away from their next job.
