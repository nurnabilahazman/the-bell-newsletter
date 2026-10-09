def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Top gold accent bar -->
  <rect x="160" y="80" width="500" height="4" rx="2" fill="#C9A84C"/>
  <!-- Large decorative quote mark -->
  <text x="152" y="200" font-size="120" fill="#e8e4db" font-weight="900" font-family="Georgia,serif">"</text>
  <!-- Three abstract content lines -->
  <rect x="220" y="180" width="420" height="24" rx="6" fill="#1A1A2E" opacity="0.12"/>
  <rect x="220" y="218" width="380" height="24" rx="6" fill="#1A1A2E" opacity="0.09"/>
  <rect x="220" y="256" width="280" height="24" rx="6" fill="#1A1A2E" opacity="0.06"/>
  <!-- Bottom gold accent bar -->
  <rect x="160" y="310" width="500" height="4" rx="2" fill="#C9A84C"/>
</svg>"""
