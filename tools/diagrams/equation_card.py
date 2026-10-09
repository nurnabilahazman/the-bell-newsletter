def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- A box -->
  <rect x="50" y="110" width="200" height="180" rx="10" fill="#1A1A2E"/>
  <text x="150" y="215" font-size="64" fill="rgba(255,255,255,0.8)" text-anchor="middle" font-weight="900">A</text>
  <!-- Plus -->
  <text x="315" y="225" font-size="52" fill="#aaa" text-anchor="middle">+</text>
  <!-- B box -->
  <rect x="370" y="110" width="200" height="180" rx="10" fill="#1A1A2E"/>
  <text x="470" y="215" font-size="64" fill="rgba(255,255,255,0.8)" text-anchor="middle" font-weight="900">B</text>
  <!-- Equals -->
  <text x="635" y="225" font-size="52" fill="#aaa" text-anchor="middle">=</text>
  <!-- Result — gold circle -->
  <circle cx="750" cy="200" r="52" fill="#C9A84C"/>
  <text x="750" y="218" font-size="44" fill="#1A1A2E" text-anchor="middle" font-weight="900">✓</text>
</svg>"""
