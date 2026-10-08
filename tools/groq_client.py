"""
One place for every Groq call in this repo.

Why this exists: Groq retired llama-3.3-70b-versatile, and every tool that had
the model name hard-coded broke at once. Now the model lives here, so the next
retirement is a one-line change.

The current model, openai/gpt-oss-120b, is a reasoning model: its thinking
counts against max_tokens. On the free tier, prompt + max_tokens must also fit
inside 8,000 tokens per minute. groq_create() handles both, and waits out the
rate limit instead of failing.

Usage (drop-in for client.chat.completions.create):
    from groq_client import groq_create
    response = groq_create(client, messages=[...], max_tokens=2000)
"""

import os
import time

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
# Used when MODEL has spent its free daily allowance (200,000 tokens per
# rolling 24 hours). Each model has its own allowance. Same gpt-oss family, so
# same settings. (qwen was rejected: it caps output at 1,000 tokens a minute.)
FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "openai/gpt-oss-20b")
TOKENS_PER_MINUTE = int(os.getenv("GROQ_TPM", "8000"))
REASONING_HEADROOM = 1500  # extra room for the model's thinking


def _estimate_tokens(messages) -> int:
    return sum(len(m.get("content", "")) for m in messages) // 3 + 50


def groq_create(client, **kwargs):
    kwargs.pop("model", None)
    messages = kwargs["messages"]
    wanted = kwargs.pop("max_tokens", 2000) + REASONING_HEADROOM
    room = TOKENS_PER_MINUTE - _estimate_tokens(messages) - 200
    kwargs["max_tokens"] = max(1000, min(wanted, room))
    kwargs.setdefault("reasoning_effort", "low")
    model = MODEL
    for attempt in range(6):
        try:
            return client.chat.completions.create(model=model, **kwargs)
        except Exception as e:
            msg = str(e)
            if "rate_limit" not in msg and "429" not in msg:
                raise
            if model == MODEL and ("per day" in msg or attempt >= 1):
                # Out of daily allowance, or still busy after one wait:
                # switch to the fallback model instead of waiting longer.
                print(f"    {MODEL} unavailable, switching to {FALLBACK_MODEL}")
                model = FALLBACK_MODEL
                continue
            wait = 20 * (attempt + 1)
            print(f"    Groq rate limit on {model}, waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Groq kept rate limiting after 6 tries")
