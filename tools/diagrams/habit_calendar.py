def render(params: dict = {}) -> str:
    cells = []
    cols = 7
    rows = 5
    cell_w, cell_h = 80, 64
    start_x, start_y = 100, 90
    gap = 8
    day_num = 0
    for r in range(rows):
        for c in range(cols):
            day_num += 1
            if day_num > 31:
                break
            x = start_x + c * (cell_w + gap)
            y = start_y + r * (cell_h + gap)
            if day_num == 22:
                cells.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="6" fill="#C9A84C"/>')
                cells.append(f'<text x="{x + cell_w//2}" y="{y + cell_h//2 + 8}" font-size="24" fill="#1A1A2E" text-anchor="middle" font-weight="900">{day_num}</text>')
            else:
                cells.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="6" fill="#e8e4db"/>')
                cells.append(f'<text x="{x + cell_w//2}" y="{y + cell_h//2 + 8}" font-size="22" fill="#bbb" text-anchor="middle">{day_num}</text>')
    grid = "\n  ".join(cells)
    return f"""<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <text x="410" y="52" font-size="20" fill="#999" text-anchor="middle" letter-spacing="2">THE HABIT</text>
  {grid}
  <text x="410" y="440" font-size="20" fill="#666" text-anchor="middle">One day that changed every week after.</text>
</svg>"""
