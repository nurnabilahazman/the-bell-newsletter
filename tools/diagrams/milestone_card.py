def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Outer decorative ring -->
  <circle cx="410" cy="200" r="168" fill="none" stroke="#e8e4db" stroke-width="3"/>
  <!-- Inner cream fill -->
  <circle cx="410" cy="200" r="148" fill="#f5f0e8"/>
  <!-- Gold accent arc (top quarter) -->
  <path d="M 410 52 A 148 148 0 0 1 558 200" fill="none" stroke="#C9A84C" stroke-width="6" stroke-linecap="round"/>
  <!-- Large bold number placeholder -->
  <text x="410" y="192" font-size="96" fill="#1A1A2E" font-weight="900" text-anchor="middle">52</text>
  <!-- Sub line -->
  <line x1="340" y1="228" x2="480" y2="228" stroke="#e0ddd7" stroke-width="1.5"/>
  <text x="410" y="258" font-size="22" fill="#aaa" text-anchor="middle" letter-spacing="2">WEEKS</text>
</svg>"""
