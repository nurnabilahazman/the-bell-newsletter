import math

def render(params: dict = {}) -> str:
    cx, cy, r_outer, r_inner = 410, 200, 158, 98
    pct = params.get("pct", 80)
    angle = (pct / 100) * 2 * math.pi - math.pi / 2
    large_arc = 1 if pct > 50 else 0
    ex = cx + r_outer * math.cos(angle)
    ey = cy + r_outer * math.sin(angle)
    ix = cx + r_inner * math.cos(angle)
    iy = cy + r_inner * math.sin(angle)
    path = (
        f"M {cx} {cy - r_outer} "
        f"A {r_outer} {r_outer} 0 {large_arc} 1 {ex:.1f} {ey:.1f} "
        f"L {ix:.1f} {iy:.1f} "
        f"A {r_inner} {r_inner} 0 {large_arc} 0 {cx} {cy - r_inner} Z"
    )
    return f"""<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="none" stroke="#e8e4db" stroke-width="60"/>
  <path d="{path}" fill="#C9A84C"/>
  <circle cx="{cx}" cy="{cy}" r="{r_inner - 2}" fill="#f5f0e8"/>
  <text x="{cx}" y="{cy + 18}" font-size="76" fill="#1A1A2E" font-weight="900" text-anchor="middle">{pct}%</text>
</svg>"""
