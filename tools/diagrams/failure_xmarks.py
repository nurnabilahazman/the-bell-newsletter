def render(params: dict = {}) -> str:
    squares = []
    xs = [120, 240, 360, 480, 600]
    labels = ["WK 1", "WK 2", "WK 3", "WK 4", "WK 5"]
    for i, (x, lbl) in enumerate(zip(xs, labels)):
        cx, cy = x + 50, 106
        squares.append(f'<text x="{cx}" y="44" font-size="17" fill="#999" text-anchor="middle" font-weight="600" letter-spacing="1">{lbl}</text>')
        squares.append(f'<rect x="{x}" y="56" width="100" height="100" rx="8" fill="#1A1A2E"/>')
        squares.append(f'<line x1="{x+12}" y1="68" x2="{x+88}" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>')
        squares.append(f'<line x1="{x+88}" y1="68" x2="{x+12}" y2="144" stroke="rgba(255,255,255,0.35)" stroke-width="2.5" stroke-linecap="round"/>')
    body = "\n  ".join(squares)
    return f"""<svg width="820" height="340" viewBox="0 0 820 340" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  {body}
  <text x="410" y="226" font-size="28" fill="#1A1A2E" font-weight="700" text-anchor="middle">Sent. Delivered. Broken.</text>
  <text x="410" y="278" font-size="22" fill="#666" text-anchor="middle">No alert. No error. Five weeks of silence.</text>
</svg>"""
