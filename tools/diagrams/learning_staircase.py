def render(params: dict = {}) -> str:
    steps = [
        ("Week 1", "One prompt", 0),
        ("Week 2", "One workflow", 1),
        ("Week 3", "One system", 2),
        ("Week 4", "Runs itself", 3),
    ]
    step_w = 160
    step_h = 60
    base_x = 80
    base_y = 340
    rects = []
    for i, (week, label, level) in enumerate(steps):
        x = base_x + i * step_w
        y = base_y - level * step_h
        w = (i + 1) * step_w
        h = (level + 1) * step_h
        is_top = i == len(steps) - 1
        fill = "#C9A84C" if is_top else "#1A1A2E"
        text_fill = "#1A1A2E" if is_top else "rgba(255,255,255,0.85)"
        rects.append(f'<rect x="{x}" y="{y}" width="{step_w - 8}" height="{step_h - 4}" rx="6" fill="{fill}"/>')
        rects.append(f'<text x="{x + (step_w - 8)//2}" y="{y + 24}" font-size="16" fill="{text_fill}" text-anchor="middle" font-weight="700">{week}</text>')
        rects.append(f'<text x="{x + (step_w - 8)//2}" y="{y + 46}" font-size="14" fill="{text_fill}" text-anchor="middle" opacity="0.8">{label}</text>')
    body = "\n  ".join(rects)
    return f"""<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <text x="410" y="44" font-size="20" fill="#999" text-anchor="middle" letter-spacing="2">THE LEARNING CURVE</text>
  {body}
  <text x="410" y="430" font-size="20" fill="#666" text-anchor="middle">Small steps. Compounding return.</text>
</svg>"""
