def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Left: BEFORE navy block -->
  <rect x="40" y="60" width="330" height="280" rx="10" fill="#1A1A2E"/>
  <text x="205" y="118" font-size="18" fill="rgba(255,255,255,0.4)" text-anchor="middle" letter-spacing="3">BEFORE</text>
  <rect x="80" y="140" width="250" height="18" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="80" y="172" width="200" height="18" rx="4" fill="rgba(255,255,255,0.1)"/>
  <rect x="80" y="204" width="220" height="18" rx="4" fill="rgba(255,255,255,0.1)"/>
  <rect x="80" y="236" width="180" height="18" rx="4" fill="rgba(255,255,255,0.08)"/>
  <rect x="80" y="268" width="210" height="18" rx="4" fill="rgba(255,255,255,0.06)"/>
  <!-- Arrow -->
  <text x="410" y="215" font-size="40" fill="#C9A84C" text-anchor="middle">→</text>
  <!-- Right: AFTER gold-border block -->
  <rect x="450" y="60" width="330" height="280" rx="10" fill="none" stroke="#C9A84C" stroke-width="2.5"/>
  <text x="615" y="118" font-size="18" fill="#C9A84C" text-anchor="middle" letter-spacing="3" font-weight="700">AFTER</text>
  <!-- Single clean gold bar = condensed result -->
  <rect x="490" y="148" width="250" height="52" rx="8" fill="#C9A84C" opacity="0.15"/>
  <rect x="490" y="148" width="250" height="52" rx="8" fill="none" stroke="#C9A84C" stroke-width="1.5"/>
  <rect x="490" y="224" width="160" height="18" rx="4" fill="#C9A84C" opacity="0.5"/>
  <rect x="490" y="256" width="120" height="18" rx="4" fill="#C9A84C" opacity="0.3"/>
  <rect x="490" y="288" width="80"  height="18" rx="4" fill="#C9A84C" opacity="0.2"/>
</svg>"""
