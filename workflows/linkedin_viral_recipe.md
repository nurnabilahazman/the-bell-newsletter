# LinkedIn Viral Post Recipe + Content-to-Subscriber Conversion Guide
**Sources:**
- Ruben Hassid LinkedIn post — "You don't need to learn to code anymore" (analyzed June 2026)
- Ruben Hassid Substack — "Vibecoding. It will never make you rich. But you still need it." (analyzed June 2026)
**Purpose:** Extract the exact mechanics behind viral LinkedIn posts AND the long-form guide that converts readers to subscribers and paying members. Both are needed for the build-in-public strategy.

---

## Why this post went viral — the real mechanics

### 1. The hook is a status grenade, not a headline

"You don't need to learn to code anymore" generates two opposite emotional reactions simultaneously:
- Coders feel threatened → comment to disagree
- Non-coders feel liberated → share to tell others

Both groups amplify it for opposite reasons. The algorithm sees high engagement from both sides and distributes it further. This is the key insight: the best hooks don't target one emotion. They create productive conflict.

**Applied to Nabilah:**
- "You don't need a data analyst to read your own data."
- "Finance teams don't use AI at work. Here's why that's about to change."
- "The report you spend 2 days writing can write itself."

---

### 2. Specificity is the entire credibility mechanism

Not "go into settings" — `Settings → Claude Code`. `Settings → Connectors`. The exact menu path.

Anyone can write "use AI to build apps." Only someone who sat in the product and clicked through every screen writes it like a command path. The specificity *is* the proof. No credentials needed. No track record needed. The detail does the work.

**Applied to Nabilah:**
- Not "use Tableau" — "SAP Fiori export → Tableau Prep flow → Tableau Desktop. Five minutes."
- Not "ask AI to write formulas" — "Type: 'Write an Excel formula that [logic]. Data is in column C.' Paste. Test. If it breaks, paste the error back."
- Not "I automated my work" — "42 hours recurring. One Excel VBA + OCR tool. Two minutes every time after."

---

### 3. The golden artifact — designed to be copied verbatim

The CEO/CTO prompt is the most-saved element of the post:

```
"You're my CTO. I'm the CEO. I don't write code and I don't read it.
Bypass is on — don't ask, just build. Interview me one question at a time
using AskUserQuestion, then build it. Use Netlify to push it live and give me a link."
```

Why it works:
- It has `[your goal]` — a placeholder. Reader inserts their context. It becomes theirs.
- It assigns roles (makes Claude commit to a mode, not just answer a question)
- It ends with a deliverable ("give me a link") — Claude knows what done looks like
- It works, out of the box, for almost anyone who pastes it

**Nabilah's golden artifacts (already exist in the 52-slide plan):**
- The weekly planning prompt (Carousel 26): `"Here are this week's tasks: [list]. Rank by urgency and impact. Suggest a day for each."`
- The report summary prompt (Carousel 19): `"Summarise this in three bullets. Each under 20 words."`
- The management summary prompt (Carousel 20): `"Here is the data. Write a management summary. 200 words. Highlight what changed vs last month."`
- The formula-building prompt (Carousel 23): `"Write an Excel formula that [logic]. Data is in [column range]."`

Every prompt post should have ONE prompt shown verbatim, formatted in a code block or indented — not described.

---

### 4. "But here's where it gets powerful:" — the reset move

Posts lose readers at ~60% of the way through. This phrase is a re-hook. It signals: everything before was setup, *here* is the actual insight. It resets attention without repeating yourself.

**Nabilah's equivalent bridges:**
- "But that's not where the time actually goes."
- "Here's the part nobody builds first (and then breaks their automation)."
- "This is where most people stop. It's also where the real savings start."

---

### 5. "Three things nobody tells you" — the insider positioning frame

This positions the creator as: *every other post on this topic is incomplete. I have what they left out.*

Rules for this section:
- Always 3. Not 5. Not 10. 3 is manageable and feels complete.
- Each tip must be screenshot-able — able to stand alone without the rest of the post
- Each tip must have a counterintuitive element. "Build one page at a time" sounds obvious until you read why (small prompts give Claude less room to break what's working)
- Use → arrows. One per tip. Scannable.
- Tip 3 should name a specific resource, URL, or action (this is the "secret" that makes the whole section feel real)

---

### 6. The reframe close — echo the hook and resolve it

Open: "You don't need to learn to code anymore."
Close: "The secret is not knowing how to code. It is knowing how to prompt."

The close answers the hook. The reader feels the loop close. It's philosophically satisfying in one line.

**Nabilah's version (applied to her carousel topics):**
- Hook: "Six hours every month. Same task. Same manual steps."
- Close: "The task didn't change. The system around it did."
- Hook: "The blank page is the most expensive part of any writing task."
- Close: "Stop starting from zero. The first draft is not your job anymore."

---

### 7. The save CTA — a whisper, not a command

`(save this if you can't code - you won't need to)`

- Lowercase. Parentheses. Bottom of post. It does not shout.
- It qualifies the reader ("if you can't code") — makes it feel personal
- It tells them exactly what to do ("save")
- Saves carry more algorithmic weight on LinkedIn than likes
- Never "smash that like button." Always: "save this" or "repost if this would have saved you time"

---

## The Full Recipe — Post Structure

```
[HOOK — 1 line]
Status grenade or identity challenge. Makes two groups react opposite ways.
Under 10 words. No context. No explanation. Just the claim.

[PROMISE — 1 line]
"Here's how to [achieve the hook promise] ([zero-effort qualifier]):"

[SETUP — numbered list, 4-7 steps]
Hyper-specific. Menu paths. Exact quotes. Real sequences.
Proves you actually did this. Each step one sentence.

[ESCALATION BRIDGE — 1 line]
"But here's where it gets powerful:" or equivalent.
Resets attention. Signals the real insight is coming.

[NUMBERED TACTICS — 2-3 items]
Start with "Stop [wrong thing]. Start [right thing]."
Or start with the exact prompt/tactic in quotes.

[GOLDEN ARTIFACT — formatted block]
The prompt, template, or formula the reader will actually copy.
Show it verbatim. Not described. Not paraphrased. Verbatim.

[PROOF POINT — 1 sentence]
"My [specific thing] went live/saved/happened in [specific time/number]."
One sentence. Specific. Can stand alone.

[INSIDER FRAME — "X things nobody tells you:"]
3 counterintuitive tips. → arrow each one.
Each must stand alone as a screenshot.
Tip 3 names a specific resource, URL, or action.

[REFRAME CLOSE — 2 sentences]
"The secret is not X. It is Y." Echoes the hook. Resolves it.
Optional: follow this with a link or resource.

[WHISPERED SAVE CTA — 1 line, lowercase, parentheses]
(save this if [reader identity] — you [payoff])
```

---

## Applied to Nabilah — Three Post Drafts Using This Recipe

### Draft A — "You don't need a data analyst to read your own data."

```
You don't need a data analyst to read your own data.

Here's how to get clear answers from any report (no jargon):

1. Open Claude. Paste the full report or data.
2. Type: "I am a finance analyst. Summarise the three most important things here. Under 20 words each."
3. Read the output. Click the source to verify.
4. If you need more: "What changed vs last month and why does it matter?"

But here's where it gets powerful:

Stop asking vague questions. Start giving Claude a role first:
"You are reviewing this for the CFO. What would she ask about?"

The output changes completely.

Paste this. Use it on the next report that lands in your inbox:
"I am a [your role] reviewing this for [your manager]. Summarise what changed, what's concerning, and what decision it requires. Under 150 words."

My KPI report review went from 45 minutes to 4 minutes.

Three things nobody tells you:

→ Claude reads tables if you paste them as plain text. Don't convert to prose first — paste raw.
→ If the summary sounds wrong, don't rephrase the question. Add context: "The business had a one-off in March that explains the drop."
→ The best prompt for any report: paste it and say "what is this really telling me?" Claude answers that differently than a summary request.

The analyst skill is not reading the data. It is knowing what question to ask.

(save this if you've ever read a 20-page report and still felt unsure what it meant)
```

### Draft B — "The formula that replaced 6 hours of work is two lines long."

```
The formula that replaced 6 hours of work is two lines long.

Here's how I built it (no coding, no IT request):

1. Write down exactly what the formula needs to do. Plain English.
2. Open Copilot in Excel. Or Claude.
3. Paste: "Write an Excel formula that [your logic]. My data is in [column range]."
4. Copy the formula. Paste it in the cell.
5. If it breaks: paste the error back. It fixes it.

But here's where it gets useful:

Stop trying to remember VLOOKUP syntax. Start describing what you need:
"I want to look up the value in column A and return the matching amount from column D."
That is the whole brief. Claude or Copilot writes the formula.

The exact prompt that built my 6-hour fix:
"Write an Excel formula that checks if the country in column B matches a list of 17 countries, and returns the KPI value in column D. Flag it red if it's more than 10% below target."

One paste. One formula. Still running.

Three things nobody tells you:

→ Copilot is already in your Excel. You don't need to download anything. Home → Copilot.
→ If the formula is complex, ask Claude to explain it line by line after. Then you actually understand what you built.
→ The formula won't break unless the column structure changes. Add a note at the top of the sheet: "Column order matters — don't reorder."

The skill is not knowing the formula. It is knowing how to describe what you need.

(save this if you've ever stared at a formula for 30 minutes that Copilot builds in 30 seconds)
```

### Draft C — "Three things nobody tells you about using AI at work."

```
Three things nobody tells you about using AI at work.

(From someone who uses it daily inside a real company)

→ The tool matters less than the context you give it.
"Summarise this" gives a mediocre summary.
"You are reviewing this for the Finance Director. Summarise the three things she'd ask about." gives a usable one.
Same tool. Different output.

→ Your company data is not the same as your personal data.
At work: use Microsoft Copilot. It stays inside the Microsoft network. Company policy, data safety, no leaks.
At home, for personal projects: Claude, ChatGPT, whatever you want.
One line in your head. Never cross it.

→ The part AI will never replace is knowing what matters.
The formula is easy. The error checking is easy. Knowing which three KPIs the CFO actually reads — that's yours.
That context lives in your relationships, not in a model.

I use AI for execution. I keep the judgment.

The two are not the same thing.

(save this if you're figuring out where the line is)
```

---

## Recipe Checklist — Before publishing any post

- [ ] Hook: under 10 words, makes two groups react opposite ways
- [ ] At least one thing in the post is shown verbatim (prompt, formula, step sequence)
- [ ] One specific proof point with a real number
- [ ] If using "3 things" frame: each tip can stand alone as a screenshot
- [ ] Close echoes and resolves the hook
- [ ] Save CTA is lowercase, in parentheses, at the bottom
- [ ] Passes the voice spec: no banned words, no banned structures
- [ ] Reader leaves with one specific thing they can do or copy today

---

## Infographic tools — honest ranking

For producing the **Ruben Hassid-style educational breakdown image** (numbered cards with content):

### 1. Canva Pro — already installed, highest control
The infographic in this post was almost certainly made in Canva. The orange circle numbers, code block styling, and card layout are all standard Canva elements.
- Search "infographic steps" or "numbered steps" in Canva templates
- Apply Bell brand colors: Cream `#F5F0E8`, Navy `#1A1A2E`, Gold `#C9A84C`
- Each "card" in the infographic = one section of the post
- Export at 1080×1080px or 1080×1350px for LinkedIn

### 2. Napkin.ai — fastest AI-native option
Paste any text. It converts it into a visual diagram automatically. The output quality is significantly better than code-generated SVGs. Free tier available.
- Paste the post content
- Choose "numbered steps" or "framework" layout
- Download as PNG or SVG
- Restyle in Canva if needed

### 3. Gamma.app — already in the stack
Works well for turning post content into visual slides. Export individual slides as images for LinkedIn.

### What to stop doing
The Python SVG diagrams in the carousel PDFs are geometric noise. They are not readable on LinkedIn. The carousels should use Canva for the visual layer — Python generates the text content and Nabilah designs the slide in Canva. The two jobs should not be done by the same tool.

---

## Part 2 — The Substack Conversion Model
**Source:** "Vibecoding. It will never make you rich. But you still need it." — Ruben Hassid, June 2026
**Question answered:** Why does one long-form guide turn readers into subscribers and paying members?

This is a different format to the LinkedIn post but it runs on many of the same principles — and adds new ones that the short-form post cannot use. Understanding this is critical because Nabilah's 5 build projects will each produce both a LinkedIn carousel series AND a potential long-form guide.

---

### 1. The subverted hook — argue against the popular claim

**What Ruben did:** Title is "Vibecoding. It will never make you rich. But you still need it."
He opens by showing screenshots of "get rich with AI" content — then says he will never sell that.

**Why it converts:** Everyone selling AI promises income. He promises honesty. In a noisy market, the person who says "I won't sell you this lie" becomes the most trusted voice immediately. The reader thinks: *if he's honest about what it won't do, I can trust what he says it will do.*

**The structure:**
```
[What everyone else is selling — name it]
"Most of it is fiction."
[What I'm actually going to give you instead]
```

**Applied to Nabilah:**
- "Everyone is posting about AI making their career easier. Most of it is performed."
- "I won't tell you AI will replace your job. I'll show you exactly what I built so mine gets easier."
- "I'm not going to tell you to learn Python. I'm going to show you how I build tools without knowing it."

---

### 2. Zero resistance model — give the gold, sell the community

**What Ruben did:** The entire guide is free. Every tool he recommends has a free tier (Netlify free, Supabase free, Claude $20/month). The paid options ($200/year Circle, enterprise training) appear only at the end, after 3,000+ words of genuine value.

**Why it converts:** The reader has already received more than they expected. By the time the paid offer appears, they are not being sold to — they are being invited further in. The subscription feels like the natural next step, not a transaction.

**The free tier list is deliberate.** "I am not affiliated" — he says this explicitly. This removes every defence the reader has. There is no angle. He is just helping.

**Rule for Nabilah:** Every tool, template, and resource in any guide should have a free option named first. The Excel formula generator you build? Free. The job calculator? Free. The save CTA should say *try this for free* not *buy this*.

---

### 3. The complete guide as product — radical generosity as marketing

**What Ruben did:** This is not a teaser. It is a working guide. You can read it, follow the 7 steps, and have something built by the end. Nothing is gated behind "subscribe to see the rest."

**Why it converts:** This is counterintuitive but well-documented. Giving away the complete guide generates more subscribers than withholding it because:
- Readers share it (it's genuinely useful, worth sharing)
- The share brings new readers who subscribe
- The subscriber wants MORE of this, not the thing they already got

**The subscription hook is embedded correctly:**
> "If you want to copy all of my prompts, subscribe to my newsletter and you will receive it for free as a gift."

He is not withholding the guide to get subscribers. He is giving MORE after the guide, as the subscribe incentive.

**Applied to Nabilah:** When you publish the "How I built the Excel Formula Generator" guide — publish the full build process, the full prompt, the tool link. Then: *"Save this. And if you want the next build before I post it publicly, subscribe to The Bell."*

---

### 4. Screenshots at every step — visual proof is the highest credibility

**What Ruben did:** The 7-step Claude Code setup has a screenshot for every single step. Not described. Shown. The exact menu. The exact button. The exact result.

**Why it converts:** A screenshot cannot be faked the same way a claim can. When you see the actual UI with the actual setting circled, you believe the author was actually there. Text says "go to Settings → Claude Code." A screenshot proves he went there.

**For LinkedIn carousels:** The S3 (mechanism) slide should ideally be a screenshot of the actual tool or step. Not an illustration. Not a diagram. The real thing. Canva can be used to annotate screenshots with arrows and labels — this is the Ruben Hassid style.

---

### 5. Multiple share triggers — engineered throughout, not just at the end

**What Ruben did:** The "Share" button appears 5 separate times in the article:
- Top (in the intro)
- After the setup section
- After the mega-prompt section
- After the "be a better vibecoder" section
- At the end

Each time it appears with a specific reason: *"Help keep this newsletter free. Share it with one person."*

**The PS at the top:** *"You must know someone who needs to be better at AI. This newsletter grows from you sharing this, for free, to this one person."* — This is not a shout. It is a quiet appeal to help someone you know. Personal. Specific. Zero pressure.

**Applied to Nabilah's LinkedIn carousels:**
- The whispered save CTA at the end (already in recipe)
- Add a mid-carousel "tag someone who does this manually" on the problem slide (S2)
- For guides: "Send this to someone in your team who still does [X] manually."

---

### 6. The honest limitation section — trust through subtraction

**What Ruben did:** Section 6 is literally called "When NOT to use Claude Code." He tells you when his own guide's subject is the wrong tool. He recommends Claude Artifacts for small tasks, Cowork for documents, ChatGPT for images — competitor tools.

**Why it converts:** This is the highest-trust signal in the entire guide. Anyone selling Claude Code would not tell you when to use ChatGPT instead. He does. The reader's sales resistance drops to zero.

**Every guide Nabilah publishes should have a "when NOT to use this" section.** For the Excel formula generator: "If your formula needs to connect to live company data, this is not the right tool — you need Power Automate instead." One line. Massive trust.

---

### 7. The secret URL tip — insider knowledge as the most saveable moment

**What Ruben did:** In the design section, he drops `getdesign.md` and `designmd.app` — two websites most people have never heard of. Free. Extremely useful. Specific.

**Why it converts:** This is the moment the reader screenshots the article. Not the overview, not the steps — the secret tool they didn't know existed. It is shareable as a standalone image. It makes the reader feel like they got something private.

**Rule:** Every guide must have at least one "this website almost nobody knows about" moment. For Nabilah's builds:
- getdesign.md (already in his guide — she can reference it too)
- napkin.ai for AI-generated diagrams
- excelfunctions.net for formula reference
- Future: tools she discovers while building her own projects

---

### 8. Real examples from real life — not invented scenarios

**What Ruben did:** His GPC consulting firm. His actual LinkedIn analytics dashboard. His actual cost habit tracker. These are his tools built for his real problems.

**Why it converts:** The reader doesn't think "could this work?" They think "he is doing this right now in a real business." Invented examples always feel slightly hollow. Real ones land.

**Applied to Nabilah:** The Bell newsletter IS her real example. She built it. It runs every week. The research brief runs every Monday. Every project she documents is something she actually uses — this is the most powerful content advantage she has.

---

### 9. The community upsell — positioned as access, not information

**What Ruben did:** The Circle ($200/year) is mentioned once, briefly, near the end. The pitch: "Direct access to me and super-smart members." Not "get information you can't get elsewhere." The information is free. The access is paid.

**This is the correct model for 2026:** Information is free everywhere. Community, feedback, and direct access are what people pay for. When Nabilah has an audience, the paid tier should be: direct access, live build sessions, early releases — not paywalled guides.

---

## Updated Nabilah Content Model — Build in Public

Based on both analyses, here is the full model for the next 100 pieces of content:

### The unit of content is a BUILD, not a topic

Every piece of content should trace back to something Nabilah actually built or is building:
- LinkedIn carousel series = the build documented in 5 slides
- Long-form guide (future newsletter issue) = the complete build walkthrough
- The tool itself = the golden artifact that drives shares

### The 5 projects and their content yield

| Project | LinkedIn carousels | Guide |
|---|---|---|
| Excel Formula Generator (web app) | 3–4 (problem → build → launch → learnings) | 1 complete "how I built this" guide |
| The Bell Newsletter (build diary) | 4–5 (pipeline, automation, tools, research brief, what broke) | 1 complete system breakdown |
| Weekly Work Summary Generator | 2–3 | 1 guide |
| "Should I Take This Job?" Calculator | 2–3 | 1 guide |
| CV Optimizer for Finance Roles | 2–3 | 1 guide |

Total minimum: 13–18 carousels + 5 guides = well over 20 pieces of content from 5 builds.

### The hook model for build content

Build content needs a different hook than the LinkedIn post recipe. The status grenade still applies — but the angle shifts:

```
[What it used to take] → [What you built] → [What it takes now]
```

Examples:
- "IT said 3 months. I gave Claude an afternoon. Here's what I built."
- "I needed a tool. I had zero budget. I vibecoded it in 2 hours. It's free."
- "I got tired of doing this manually. So I built the thing that does it for me."

Two groups react: people who are still waiting for IT / still doing it manually (feel seen) + people who think this isn't possible for non-coders (feel challenged).

### Zero resistance pricing model

Following Ruben's model exactly:
- The tools Nabilah builds: **free to use**
- The guides she writes: **free to read**
- The paid tier (when audience exists): **community + direct access + early builds**

This is not a sacrifice. Free tools with her name on them are the most powerful distribution mechanism available. Every person who uses the Excel Formula Generator is a potential subscriber.

---

## Updated Recipe Checklist — before publishing any build post

- [ ] Hook: under 10 words, creates two opposing reactions, does NOT promise money
- [ ] The build is real — something she actually made and uses
- [ ] At least one thing shown verbatim: the prompt, the code snippet, the tool link
- [ ] One honest limitation ("this doesn't work if...")
- [ ] One secret URL or resource the reader didn't know existed
- [ ] Screenshots over descriptions wherever possible (especially S3 in carousels)
- [ ] Mid-content share trigger: "tag someone who does this manually"
- [ ] End save CTA: lowercase, parentheses, specific identity ("save this if you still...")
- [ ] Close echoes and resolves the hook
- [ ] If a tool was built: the link is in the post, it works, it's free to try

---

*Last updated: June 2026 — Substack analysis added. Pivot from finance automation to build-in-public model confirmed.*
