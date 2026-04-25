# Section 3 — SaaS Guide
## Building Bell Transcript: From Idea to Paying Customers

---

### What We're Building

**Bell Transcript** — a web app that extracts transcripts from YouTube videos and podcasts, then generates structured AI summaries.

**The problem it solves:** Watching a 1-hour video to get 3 key points wastes time. Bell Transcript gives you the summary in 30 seconds.

**Business model:**
- Free tier: 3 transcripts per month
- Pro: $9/month — unlimited transcripts, longer summaries, export to PDF/Notion
- Target customer: content creators, students, researchers, busy professionals

---

### Why This Idea Has Demand

- YouTube has 800 million videos. People can't watch everything.
- Existing tools (Otter.ai, Descript) are expensive ($17–$30/month) and complex
- A simple, cheap alternative has a clear market
- Week 4 of the project curriculum already teaches the core technical skill

**Competitors to study:**
| Tool | Price | Weakness |
|---|---|---|
| Otter.ai | $17/month | Expensive, overkill for simple use |
| Tactiq | $8/month | Chrome extension only, no app |
| NoteGPT | $9/month | Cluttered UI, poor mobile |
| YouTube auto-captions | Free | No summarisation, just raw text |

**Your angle:** Cheaper than Otter, simpler than Descript, better mobile UX than all of them.

---

### The 8-Week Build Roadmap

| Week | Task | Deliverable |
|---|---|---|
| 1 | Competitor research + define your unique angle | Written positioning doc |
| 2 | Build core transcript extraction script | Working Python script |
| 3 | Build simple web interface (Flask) | Working local web app |
| 4 | Add user accounts (sign up, login, usage tracking) | Auth system working |
| 5 | Add Stripe payment ($9/month Pro plan) | Payment processing live |
| 6 | Deploy to internet + domain + landing page | Live at your domain |
| 7 | Get first 10 users (Reddit + direct outreach) | Real users signed up |
| 8 | First revenue review + iteration | Paying customers or clear feedback |

---

### Tech Stack (all free to start)

| Layer | Tool | Cost |
|---|---|---|
| Language | Python | Free |
| Web framework | Flask | Free |
| Transcript extraction | youtube-transcript-api | Free |
| AI summarisation | Groq API | Free tier |
| Database | SQLite (local) → PostgreSQL (production) | Free |
| Hosting | Railway.app or Render.com | Free tier available |
| Payments | Stripe | 2.9% + 30¢ per transaction (no monthly fee) |
| Domain | Namecheap | ~$10/year |

**Total cost to launch: ~$10** (just the domain)

---

### How to Work With Claude on SaaS Tasks

Each week's SaaS section includes a task prompt. Here's how to use it:

1. **Paste the prompt into a fresh Claude conversation**
2. **Tell Claude your current setup** — what's already built, what's working, what broke
3. **Work through the task step by step** — don't rush to the next week's task
4. **Save every working file** — keep a `/bell-transcript/` folder in your projects

**When Claude gives you code to run, test it immediately.** Don't accumulate untested code.

---

### Tracking Progress

Update `config/saas_progress.json` each week:
- Change `"current_week"` to the next number
- Mark `"completed": true` on the finished milestone
- Add notes on what you learned

The newsletter automatically picks up the next task.

---

### Getting Your First Customers

**Don't wait until the product is perfect.** Launch at Week 6 even if it's basic.

**Where to find first users:**
- **r/productivity**, **r/youtubers**, **r/contentcreation** — post genuinely helpful content, mention your tool
- **Direct outreach** — find 10 YouTubers with 1K–50K subscribers, email them: "I built a tool that summarises YouTube videos — want to try it free?"
- **Product Hunt** — launch there on Week 7 for visibility
- **Your own network** — tell people you're building it

**The goal for Week 7 is 10 free users, not 10 paying users.** Get feedback first.

---

### Revenue Milestones to Aim For

| Milestone | What it means |
|---|---|
| First free user | Your product works |
| 10 free users | People find it useful |
| First paid user | Someone values it enough to pay |
| 10 paid users ($90 MRR) | You have a real product |
| 50 paid users ($450 MRR) | Worth investing more time |
| 100 paid users ($900 MRR) | Quit-your-job territory (eventually) |

---

### Useful Resources

- **Flask quickstart:** flask.palletsprojects.com/quickstart
- **Stripe integration guide:** stripe.com/docs/billing/quickstart
- **Railway hosting (free tier):** railway.app
- **Indie hackers (SaaS stories):** indiehackers.com
- **Starter Story (how people built products):** starterstory.com
