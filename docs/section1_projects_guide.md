# Section 1 — Projects Guide
## How to Work With Claude to Build Each Week's Project

---

### How This Works
Each week you get a detailed prompt. Paste it into Claude (claude.ai — your Pro subscription). Claude will guide you step by step. Your job is to follow the instructions, run the commands it gives you, and ask follow-up questions when something doesn't work.

You are not expected to understand every line of code. You are expected to understand what the tool does and how to run it.

---

### Before You Start Each Project

**Open a fresh Claude conversation.** Don't continue from a previous chat — start clean so Claude has full context from your prompt.

**Read the prompt before pasting.** Spend 2 minutes reading it so you understand what you're about to build. Then paste the whole thing.

**Have VS Code open.** Claude will tell you what files to create. Use VS Code to create them and paste the code in.

**Have Terminal ready.** Claude will give you `pip install` and `python3` commands to run.

---

### During the Build

**If Claude gives you code, run it immediately.** Don't save it for later. Test as you go.

**If you get an error, paste the full error back to Claude.** Don't describe it — paste it. Claude will fix it.

**If Claude asks you a question, answer it specifically.** "I want it to save to Google Sheets" is better than "whatever you think is best."

**Don't skip steps.** If Claude says "now set up a service account", do it before continuing.

---

### Common Issues and Fixes

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip3 install [module name]` in terminal |
| `FileNotFoundError` | Check your current directory — run `cd` to confirm you're in the Newsletter folder |
| Script runs but does nothing | Check that your `.env` file is saved and the API keys are filled in |
| Output file not created | Look for a `.tmp/` folder — it gets created automatically on first run |
| Claude's code has a bug | Paste the error back to Claude with "I got this error when I ran your code" |

---

### After You Finish

1. Tick the **✓ Built** checkbox in your Bell Newsletter Tracker Google Sheet
2. Save the working script — it's your portfolio
3. Note anything you learned or struggled with — useful context for next week

---

### The 12-Week Learning Arc

| Weeks | Focus |
|---|---|
| 1–3 | Basics: automation, data collection, document generation |
| 4–6 | APIs: connecting to external services, monitoring, alerts |
| 7–9 | AI integration: content, images, data extraction |
| 10–12 | Putting it all together: reports, dashboards, full systems |

By Week 12 you will have built 12 working tools and understand how to connect any service to any other service using Python and AI.

---

### Useful Resources

- **Python basics (free):** python.org/about/gettingstarted
- **VS Code shortcuts:** code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf
- **pip package search:** pypi.org
- **When stuck on code:** stackoverflow.com
