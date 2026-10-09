S-22 · Secrets & environment variables (.env) · The Bell

You think that test code is gone. It's not.

Anything hardcoded into your code stays there, forever, in your project's history, even if you delete it later.

Every lesson on my site follows the exact same shape:

✦ Read the idea. 1 minute, plain English, no jargon.
✦ Try it live in the browser. No install, no account.
✦ A 2 question quiz. Confirms it actually landed.
✦ A real project you keep. Not a toy example.

Lesson twenty two, as proof it's real:

echo ".env" >> .gitignore

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

The key lives in .env, and .gitignore keeps .env off GitHub. The same pattern behind every tool on my site.

25 lessons. Mapped start to finish, so you always know what's next and nothing gets skipped.

Step 1. Open lesson twenty two: https://the-bell.onrender.com/syllabus/lesson/S-22/
Step 2. Read it. 1 minute.
Step 3. Try it live. 1 minute.
Step 4. Take the quiz. 1 minute.

3 minutes, during the coffee you're already making.

Free. No login.

♻️ Repost this for someone one skill away from their next job.
