def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Left column: navy -->
  <rect x="50" y="60" width="330" height="280" rx="10" fill="#1A1A2E"/>
  <text x="215" y="110" font-size="18" fill="rgba(255,255,255,0.35)" text-anchor="middle" letter-spacing="3">WITHOUT</text>
  <rect x="90"  y="138" width="250" height="16" rx="4" fill="rgba(255,255,255,0.12)"/>
  <rect x="90"  y="168" width="200" height="16" rx="4" fill="rgba(255,255,255,0.09)"/>
  <rect x="90"  y="198" width="230" height="16" rx="4" fill="rgba(255,255,255,0.07)"/>
  <rect x="90"  y="228" width="180" height="16" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="90"  y="258" width="210" height="16" rx="4" fill="rgba(255,255,255,0.04)"/>
  <!-- Right column: gold border -->
  <rect x="440" y="60" width="330" height="280" rx="10" fill="none" stroke="#C9A84C" stroke-width="2.5"/>
  <text x="605" y="110" font-size="18" fill="#C9A84C" text-anchor="middle" letter-spacing="3" font-weight="700">WITH</text>
  <rect x="480" y="138" width="250" height="16" rx="4" fill="#C9A84C" opacity="0.6"/>
  <rect x="480" y="168" width="250" height="16" rx="4" fill="#C9A84C" opacity="0.45"/>
  <rect x="480" y="198" width="250" height="16" rx="4" fill="#C9A84C" opacity="0.3"/>
  <rect x="480" y="228" width="250" height="16" rx="4" fill="#C9A84C" opacity="0.2"/>
  <rect x="480" y="258" width="250" height="16" rx="4" fill="#C9A84C" opacity="0.12"/>
</svg>"""
