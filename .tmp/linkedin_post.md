# LinkedIn Post — Week 1
# Type: building_from_zero
# Generated: 2026-10-11 20:44

---

My auto‑reply sent a “thanks for contacting us” to a complaint about a broken link.  

I set Claude to read incoming mail, tag it, then draft a reply. The tag worked, the draft didn’t.  

The prompt I gave Claude missed the “subject line” token, so it generated a generic reply.  

I spent 3 hours fixing the prompt, then watched the system fire on a real email. It finally sent a proper “we’re on it” reply.  

The Stripe integration for the $9 / month Pro plan also broke on the test card. The error was “invalid secret key” – I’d copied the test key from the dashboard but pasted a stray space.  

After clearing the space, the payment succeeded. No users yet, but the flow works end‑to‑end.  

Lesson: the tiniest typo can stall an entire feature.  

If you’re coding from zero, expect these tiny roadblocks.  

Follow — I post every week on building with Claude from Malaysia.
