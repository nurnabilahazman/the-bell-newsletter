"""
S-05: LinkedIn Post Character Counter
Paste your draft between the quotes, run it, and check it against
LinkedIn's 3,000 character limit.
"""

post = "Automated my monthly KPI pack. Saved 8 hours a month."

characters = len(post)
words = len(post.split())
over_limit = characters > 3000

print(f"Characters: {characters}")
print(f"Words: {words}")
print(f"Over the 3,000 limit? {over_limit}")
