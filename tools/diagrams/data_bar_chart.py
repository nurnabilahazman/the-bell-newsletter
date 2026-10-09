def render(params: dict = {}) -> str:
    bars = [
        (520, 0.9, True),   # longest — gold, focal
        (320, 0.55, False),
        (180, 0.35, False),
        (80,  0.2,  False),
    ]
    rects = []
    y_start = 80
    h = 52
    gap = 16
    for i, (w, op, is_focal) in enumerate(bars):
        y = y_start + i * (h + gap)
        fill = "#C9A84C" if is_focal else "#1A1A2E"
        opacity = str(op) if not is_focal else "1"
        rects.append(f'<rect x="160" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" opacity="{opacity}"/>')
    body = "\n  ".join(rects)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
  <line x1="160" y1="360" x2="720" y2="360" stroke="#e0ddd7" stroke-width="1"/>
</svg>"""
