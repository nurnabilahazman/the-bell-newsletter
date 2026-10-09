def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Layer 3: bottom, widest, most faded -->
  <rect x="110" y="290" width="600" height="56" rx="8" fill="#1A1A2E" opacity="0.3"/>
  <text x="410" y="325" font-size="20" fill="rgba(255,255,255,0.5)" text-anchor="middle" letter-spacing="2">SOURCE</text>
  <!-- Layer 2: mid -->
  <rect x="70"  y="218" width="680" height="56" rx="8" fill="#1A1A2E" opacity="0.6"/>
  <text x="410" y="253" font-size="20" fill="rgba(255,255,255,0.75)" text-anchor="middle" letter-spacing="2">PROCESS</text>
  <!-- Layer 1: top, gold, narrowest — focal point -->
  <rect x="30"  y="146" width="760" height="56" rx="8" fill="#C9A84C"/>
  <text x="410" y="181" font-size="20" fill="#1A1A2E" text-anchor="middle" letter-spacing="2" font-weight="800">OUTPUT</text>
</svg>"""
