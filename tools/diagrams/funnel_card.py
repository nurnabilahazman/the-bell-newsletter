def render(params: dict = {}) -> str:
    layers = [620, 460, 280, 130]
    rects = []
    y_start = 56
    h = 58
    gap = 10
    for i, w in enumerate(layers):
        x = (820 - w) // 2
        y = y_start + i * (h + gap)
        is_last = i == len(layers) - 1
        fill = "#C9A84C" if is_last else f"rgba(26,26,46,{0.3 + i * 0.18:.2f})"
        rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"/>')
    body = "\n  ".join(rects)
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
</svg>"""
