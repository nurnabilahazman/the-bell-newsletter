def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- BEFORE side — faded large block -->
  <rect x="60" y="80" width="300" height="240" rx="10" fill="#e8e4db"/>
  <text x="210" y="176" font-size="22" fill="#bbb" text-anchor="middle" letter-spacing="3">BEFORE</text>
  <rect x="100" y="198" width="220" height="16" rx="4" fill="#d4cfc4"/>
  <rect x="120" y="226" width="180" height="16" rx="4" fill="#d4cfc4"/>
  <rect x="140" y="254" width="140" height="16" rx="4" fill="#d4cfc4"/>
  <!-- Arrow -->
  <text x="410" y="215" font-size="44" fill="#C9A84C" text-anchor="middle">→</text>
  <!-- AFTER side — gold accent -->
  <rect x="460" y="80" width="300" height="240" rx="10" fill="none" stroke="#C9A84C" stroke-width="3"/>
  <text x="610" y="176" font-size="22" fill="#C9A84C" text-anchor="middle" letter-spacing="3" font-weight="700">AFTER</text>
  <!-- Single clean bar = simplified -->
  <rect x="500" y="198" width="220" height="40" rx="6" fill="#C9A84C" opacity="0.25"/>
  <rect x="500" y="198" width="140" height="40" rx="6" fill="#C9A84C"/>
</svg>"""
