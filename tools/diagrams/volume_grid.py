def render(params: dict = {}) -> str:
    cols, rows, sq, gap = 13, 4, 48, 8
    total_w = cols * sq + (cols - 1) * gap
    ox = (820 - total_w) // 2
    oy = 90
    rects = []
    for r in range(rows):
        for c in range(cols):
            x = ox + c * (sq + gap)
            y = oy + r * (sq + gap)
            rects.append(f'<rect x="{x}" y="{y}" width="{sq}" height="{sq}" rx="5" fill="#C9A84C"/>')
    grid = "\n  ".join(rects)
    return f"""<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <text x="410" y="46" font-size="20" fill="#666" text-anchor="middle" font-style="italic">One square = one newsletter</text>
  {grid}
  <line x1="50" y1="350" x2="770" y2="350" stroke="#ddd8cf" stroke-width="1"/>
  <text x="50" y="402" font-size="26" fill="#1A1A2E" font-weight="700">52 newsletters / year</text>
  <text x="770" y="402" font-size="26" fill="#C9A84C" font-weight="900" text-anchor="end">0 hrs effort</text>
</svg>"""
