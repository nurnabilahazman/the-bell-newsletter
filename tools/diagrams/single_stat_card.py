def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Three concentric rings — abstract volume indicator -->
  <circle cx="410" cy="200" r="180" fill="none" stroke="#e8e4db" stroke-width="3"/>
  <circle cx="410" cy="200" r="130" fill="none" stroke="#d4cfc4" stroke-width="3"/>
  <circle cx="410" cy="200" r="80"  fill="#C9A84C"/>
  <!-- Gold inner dot -->
  <circle cx="410" cy="200" r="30" fill="#1A1A2E"/>
  <!-- Arrow pointing right — abstract "change" indicator -->
  <text x="410" y="215" font-size="36" fill="#f5f0e8" text-anchor="middle" font-weight="900">→</text>
</svg>"""
