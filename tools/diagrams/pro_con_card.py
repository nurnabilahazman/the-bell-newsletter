def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Left: X column, navy header -->
  <rect x="50" y="60" width="320" height="52" rx="8" fill="#1A1A2E"/>
  <text x="210" y="93" font-size="18" fill="rgba(255,255,255,0.6)" text-anchor="middle" letter-spacing="3">OLD WAY</text>
  <text x="80"  y="158" font-size="28" fill="#aaa">✕</text><rect x="120" y="140" width="220" height="20" rx="5" fill="#e0dbd0"/>
  <text x="80"  y="208" font-size="28" fill="#aaa">✕</text><rect x="120" y="190" width="200" height="20" rx="5" fill="#e0dbd0"/>
  <text x="80"  y="258" font-size="28" fill="#aaa">✕</text><rect x="120" y="240" width="210" height="20" rx="5" fill="#e0dbd0"/>
  <text x="80"  y="308" font-size="28" fill="#aaa">✕</text><rect x="120" y="290" width="190" height="20" rx="5" fill="#e0dbd0"/>
  <!-- Divider -->
  <line x1="410" y1="60" x2="410" y2="360" stroke="#e0ddd7" stroke-width="1.5"/>
  <!-- Right: check column, gold header -->
  <rect x="450" y="60" width="320" height="52" rx="8" fill="#C9A84C"/>
  <text x="610" y="93" font-size="18" fill="#1A1A2E" text-anchor="middle" letter-spacing="3" font-weight="800">NEW WAY</text>
  <text x="465" y="158" font-size="28" fill="#C9A84C">✓</text><rect x="505" y="140" width="220" height="20" rx="5" fill="#C9A84C" opacity="0.3"/>
  <text x="465" y="208" font-size="28" fill="#C9A84C">✓</text><rect x="505" y="190" width="220" height="20" rx="5" fill="#C9A84C" opacity="0.25"/>
  <text x="465" y="258" font-size="28" fill="#C9A84C">✓</text><rect x="505" y="240" width="220" height="20" rx="5" fill="#C9A84C" opacity="0.2"/>
  <text x="465" y="308" font-size="28" fill="#C9A84C">✓</text><rect x="505" y="290" width="220" height="20" rx="5" fill="#C9A84C" opacity="0.15"/>
</svg>"""
