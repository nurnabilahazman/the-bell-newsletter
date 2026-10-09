def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- MYTH row — faded, strikethrough -->
  <rect x="80" y="60" width="660" height="100" rx="10" fill="#f0ece3"/>
  <text x="180" y="107" font-size="18" fill="#bbb" letter-spacing="3">MYTH</text>
  <rect x="280" y="95" width="400" height="20" rx="4" fill="#d4cfc4"/>
  <!-- Strikethrough -->
  <line x1="100" y1="110" x2="720" y2="110" stroke="#cc4444" stroke-width="2.5" stroke-linecap="round" opacity="0.5"/>
  <!-- Down arrow -->
  <text x="410" y="200" font-size="36" fill="#aaa" text-anchor="middle">↓</text>
  <!-- REALITY row — navy + gold -->
  <rect x="80" y="220" width="660" height="120" rx="10" fill="#1A1A2E"/>
  <text x="180" y="268" font-size="18" fill="#C9A84C" letter-spacing="3" font-weight="700">REALITY</text>
  <rect x="280" y="255" width="400" height="22" rx="4" fill="rgba(201,168,76,0.4)"/>
  <rect x="280" y="291" width="300" height="16" rx="4" fill="rgba(255,255,255,0.1)"/>
</svg>"""
