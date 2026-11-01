# LinkedIn Post — Week 4
# Type: tool_tip
# Generated: 2026-11-01 20:56

---

Most people ask Claude “summarize this PDF” and get a wall of text with no page numbers.  

I tried that last night, got a 2‑page dump, then realized I needed the exact location for each answer.  

The fix is a single prompt that tells Claude to treat the uploaded file as a searchable knowledge base and always return the source page.  

Here’s the prompt I use:

```
You are a helpful assistant. I will upload a PDF.  
When I ask a question, search the document, give a concise answer, and end with “Source: page X”.  
If the answer isn’t in the file, say “I don’t know”.  
Only use information from the PDF.
```

Upload any PDF, paste the prompt, then ask, e.g., “What is the refund policy?” and Claude replies with the answer **and** “Source: page 7”.  

No code, no extra tools – just Claude’s built‑in file handling.  

Save this prompt, paste it next time you need a Q&A bot that actually points to the right page.  

♻️ Repost if this would save you time.
