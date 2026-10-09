S-13 · Modules & imports · The Bell

You think you have to build this yourself. You really don't.

Someone already wrote the hard part. Importing it takes one line, no reinventing anything.

Every lesson on my site follows the exact same shape:

✦ Read the idea. 1 minute, plain English, no jargon.
✦ Try it live in the browser. No install, no account.
✦ A 2 question quiz. Confirms it actually landed.
✦ A real project you keep. Not a toy example.

Lesson thirteen, as proof it's real:

import secrets
import string

characters = string.ascii_letters + string.digits + string.punctuation
password = ""
for i in range(12):
    password = password + secrets.choice(characters)

A real secure password generator, built on two modules that already ship with Python. secrets, not random, because passwords need randomness nobody can predict.

25 lessons. Mapped start to finish, so you always know what's next and nothing gets skipped.

Step 1. Open lesson thirteen: https://the-bell.onrender.com/syllabus/lesson/S-13/
Step 2. Read it. 1 minute.
Step 3. Try it live. 1 minute.
Step 4. Take the quiz. 1 minute.

3 minutes, during the coffee you're already making.

Free. No login.

♻️ Repost this for someone one skill away from their next job.
