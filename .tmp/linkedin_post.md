# LinkedIn Post — Week 2
# Type: system_reveal
# Generated: 2026-10-18 19:10

---

My first price‑monitor script sent me an empty email at 3 am because the selector was wrong.  

I spent 4 hours tweaking the CSS path until Claude finally pulled the right element from the product page.  

Now the script checks a shoes store every 10 minutes, compares the price to my RM150 target, and fires an email if it drops.  

The whole thing runs on a free Glitch server – zero cost, just a tiny RM0.10 monthly for the custom domain.  

Steps:  
→ Claude writes the Python fetcher. → I add a simple if‑statement: “if price < 150 → send email.” → I schedule it with a cron job (Claude sets the cron syntax).  

The email itself is plain text: “Price alert – shoes now RM149.99”. No fancy HTML, just what I need to act fast.  

It took 2 days from idea to live alert, and I’ve already saved RM20 on a pair I was eyeing.  

If you can copy‑paste a few lines and set a cron, you can stop overpaying on anything you track.  

♻️ Repost if this would have saved you a purchase.
