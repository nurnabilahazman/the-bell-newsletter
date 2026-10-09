def render(params: dict = {}) -> str:
    items = []
    n = 4
    cx = 130
    y_start = 80
    y_step = 82
    for i in range(n):
        y = y_start + i * y_step
        is_last = i == n - 1
        dot_fill = "#C9A84C" if is_last else "#1A1A2E"
        line_col = "#ddd8cf"
        if i < n - 1:
            items.append(f'<line x1="{cx}" y1="{y + 16}" x2="{cx}" y2="{y + y_step}" stroke="{line_col}" stroke-width="2"/>')
        items.append(f'<circle cx="{cx}" cy="{y}" r="14" fill="{dot_fill}"/>')
        bar_fill = "#C9A84C" if is_last else "#1A1A2E"
        bar_op = "0.8" if is_last else f"{0.15 + i * 0.12:.2f}"
        bar_w = 420 - i * 30 if not is_last else 460
        items.append(f'<rect x="{cx + 36}" y="{y - 12}" width="{bar_w}" height="26" rx="6" fill="{bar_fill}" opacity="{bar_op}"/>')
    body = "\n  ".join(items)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
</svg>"""
