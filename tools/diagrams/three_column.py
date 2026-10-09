def render(params: dict = {}) -> str:
    labels = ["01", "02", "03"]
    col_w, col_h = 220, 240
    gap = 30
    total_w = len(labels) * col_w + (len(labels) - 1) * gap
    start_x = (820 - total_w) // 2
    y = 90
    rects = []
    for i, label in enumerate(labels):
        x = start_x + i * (col_w + gap)
        is_last = i == len(labels) - 1
        fill = "#C9A84C" if is_last else "#1A1A2E"
        num_fill = "#1A1A2E" if is_last else "#C9A84C"
        rects.append(f'<rect x="{x}" y="{y}" width="{col_w}" height="{col_h}" rx="10" fill="{fill}"/>')
        rects.append(f'<text x="{x + col_w//2}" y="{y + 90}" font-size="52" fill="{num_fill}" text-anchor="middle" font-weight="900">{label}</text>')
        rects.append(f'<rect x="{x + 24}" y="{y + 136}" width="{col_w - 48}" height="14" rx="4" fill="{num_fill}" opacity="0.25"/>')
        rects.append(f'<rect x="{x + 24}" y="{y + 162}" width="{col_w - 68}" height="14" rx="4" fill="{num_fill}" opacity="0.15"/>')
    body = "\n  ".join(rects)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
</svg>"""
