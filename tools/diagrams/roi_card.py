def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Small INPUT box -->
  <rect x="60" y="110" width="200" height="180" rx="10" fill="#1A1A2E"/>
  <text x="160" y="190" font-size="18" fill="rgba(255,255,255,0.4)" text-anchor="middle" letter-spacing="2">INPUT</text>
  <rect x="90" y="210" width="140" height="16" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="90" y="238" width="110" height="16" rx="4" fill="rgba(255,255,255,0.1)"/>
  <!-- Multiplier arrow -->
  <text x="340" y="210" font-size="44" fill="#C9A84C" text-anchor="middle" font-weight="900">×</text>
  <!-- Large OUTPUT box — gold -->
  <rect x="420" y="70" width="340" height="260" rx="10" fill="none" stroke="#C9A84C" stroke-width="3"/>
  <text x="590" y="158" font-size="18" fill="#C9A84C" text-anchor="middle" letter-spacing="2" font-weight="700">OUTPUT</text>
  <rect x="456" y="178" width="268" height="28" rx="6" fill="#C9A84C" opacity="0.4"/>
  <rect x="456" y="220" width="268" height="28" rx="6" fill="#C9A84C" opacity="0.3"/>
  <rect x="456" y="262" width="268" height="28" rx="6" fill="#C9A84C" opacity="0.2"/>
</svg>"""
