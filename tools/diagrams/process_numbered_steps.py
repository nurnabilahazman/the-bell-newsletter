def render(params: dict = {}) -> str:
    return """<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Step 1 -->
  <circle cx="190" cy="190" r="64" fill="#1A1A2E"/>
  <text x="190" y="208" font-size="56" fill="#fff" text-anchor="middle" font-weight="900">1</text>
  <!-- Step 2 -->
  <circle cx="410" cy="190" r="64" fill="#1A1A2E"/>
  <text x="410" y="208" font-size="56" fill="#fff" text-anchor="middle" font-weight="900">2</text>
  <!-- Step 3 — gold focal point -->
  <circle cx="630" cy="190" r="64" fill="#C9A84C"/>
  <text x="630" y="208" font-size="56" fill="#1A1A2E" text-anchor="middle" font-weight="900">3</text>
  <!-- Connectors -->
  <line x1="254" y1="190" x2="346" y2="190" stroke="#ddd8cf" stroke-width="2"/>
  <polygon points="346,183 360,190 346,197" fill="#ddd8cf"/>
  <line x1="474" y1="190" x2="566" y2="190" stroke="#ddd8cf" stroke-width="2"/>
  <polygon points="566,183 580,190 566,197" fill="#ddd8cf"/>
  <!-- Labels -->
  <text x="190" y="292" font-size="22" fill="#666" text-anchor="middle">Extract</text>
  <text x="410" y="292" font-size="22" fill="#666" text-anchor="middle">Clean</text>
  <text x="630" y="292" font-size="22" fill="#1A1A2E" text-anchor="middle" font-weight="700">Report</text>
  <!-- Bottom caption -->
  <text x="410" y="400" font-size="22" fill="#666" text-anchor="middle">Three steps. One pipeline. Done.</text>
</svg>"""
