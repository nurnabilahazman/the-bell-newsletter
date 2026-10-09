def render(params: dict = {}) -> str:
    steps = ["01", "02", "03", "04"]
    box_w, box_h = 148, 80
    gap = 36
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    start_x = (820 - total_w) // 2
    y = 160
    boxes = []
    for i, label in enumerate(steps):
        x = start_x + i * (box_w + gap)
        is_last = i == len(steps) - 1
        fill = "#C9A84C" if is_last else "#1A1A2E"
        text_fill = "#1A1A2E" if is_last else "rgba(255,255,255,0.85)"
        boxes.append(f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="{fill}"/>')
        boxes.append(f'<text x="{x + box_w//2}" y="{y + box_h//2 + 12}" font-size="32" fill="{text_fill}" text-anchor="middle" font-weight="900">{label}</text>')
        if not is_last:
            ax = x + box_w + gap // 2
            boxes.append(f'<text x="{ax}" y="{y + box_h//2 + 12}" font-size="30" fill="#C9A84C" text-anchor="middle">›</text>')
    body = "\n  ".join(boxes)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
</svg>"""
