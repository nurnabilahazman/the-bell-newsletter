def render(params: dict = {}) -> str:
    rows = []
    items = [True, True, True, False]
    for i, done in enumerate(items):
        y = 100 + i * 76
        if done:
            rows.append(f'<rect x="100" y="{y}" width="48" height="48" rx="8" fill="#C9A84C"/>')
            rows.append(f'<text x="124" y="{y + 33}" font-size="26" fill="#1A1A2E" text-anchor="middle" font-weight="900">✓</text>')
            rows.append(f'<rect x="168" y="{y + 10}" width="{320 - i*40}" height="20" rx="5" fill="#1A1A2E" opacity="0.15"/>')
        else:
            rows.append(f'<rect x="100" y="{y}" width="48" height="48" rx="8" fill="none" stroke="#ddd8cf" stroke-width="2"/>')
            rows.append(f'<rect x="168" y="{y + 10}" width="200" height="20" rx="5" fill="#ddd8cf"/>')
    body = "\n  ".join(rows)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
</svg>"""
