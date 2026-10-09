def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Terminal frame -->
  <rect x="60" y="50" width="700" height="300" rx="12" fill="#1A1A2E"/>
  <!-- Title bar -->
  <rect x="60" y="50" width="700" height="42" rx="12" fill="#0f0f1a"/>
  <rect x="60" y="80" width="700" height="12" fill="#0f0f1a"/>
  <circle cx="94"  cy="71" r="7" fill="#ff5f56"/>
  <circle cx="116" cy="71" r="7" fill="#ffbd2e"/>
  <circle cx="138" cy="71" r="7" fill="#27c93f"/>
  <!-- Prompt symbol -->
  <text x="96" y="134" font-size="18" fill="#C9A84C" font-family="monospace">›</text>
  <!-- Three abstract content lines -->
  <rect x="120" y="120" width="500" height="16" rx="4" fill="rgba(255,255,255,0.2)"/>
  <rect x="120" y="160" width="440" height="16" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="120" y="200" width="380" height="16" rx="4" fill="rgba(255,255,255,0.1)"/>
  <rect x="120" y="240" width="300" height="16" rx="4" fill="rgba(255,255,255,0.07)"/>
  <!-- Blinking cursor -->
  <rect x="120" y="272" width="12" height="20" rx="2" fill="#C9A84C" opacity="0.8"/>
</svg>"""
