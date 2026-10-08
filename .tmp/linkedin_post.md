# LinkedIn Post — Week 1
# Type: building_from_zero
# Generated: 2026-10-08 16:09

---

The YouTube API returned a 401 error the first time I tried to pull video data. I had only read the docs, no code yet.  
I set up a simple script in Python and ran it. The error stopped at the authentication step.  
I googled “YouTube 401 error” and found that the key was missing a scope.  
I added the scope and re‑ran. It fetched the video title, but the transcript was still empty.  
I discovered the transcript is a separate endpoint; I had to call it after the video ID.  
I wrote a loop to hit the transcript URL. It returned JSON with timestamps and text.  
I passed that JSON into Claude for summarisation. Claude produced a 200‑word summary.  
I saved the result in a database but forgot to set up user authentication, so the app crashed when two users tried to sign up.  
I added a simple email‑password login with Firebase Auth. Now each user can track how many transcripts they’ve used.  
No live demo yet, but the core flow works: YouTube → API → Claude → DB.  
Follow — I post every week on building with Claude from Malaysia.
