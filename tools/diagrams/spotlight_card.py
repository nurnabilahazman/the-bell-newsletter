def render(params: dict = {}) -> str:
    return """<svg width="820" height="420" viewBox="0 0 820 420" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Outer rings — fading -->
  <circle cx="410" cy="200" r="178" fill="none" stroke="#e8e4db" stroke-width="1.5"/>
  <circle cx="410" cy="200" r="138" fill="none" stroke="#ddd8cf" stroke-width="1.5"/>
  <circle cx="410" cy="200" r="98"  fill="none" stroke="#d4cfc4" stroke-width="1.5"/>
  <!-- Gold center -->
  <circle cx="410" cy="200" r="66" fill="#C9A84C"/>
  <circle cx="410" cy="200" r="28" fill="#1A1A2E"/>
  <!-- Radiating tick marks at 4 compass points -->
  <line x1="410" y1="18"  x2="410" y2="34"  stroke="#C9A84C" stroke-width="2"/>
  <line x1="590" y1="200" x2="574" y2="200" stroke="#C9A84C" stroke-width="2"/>
  <line x1="410" y1="382" x2="410" y2="366" stroke="#C9A84C" stroke-width="2"/>
  <line x1="230" y1="200" x2="246" y2="200" stroke="#C9A84C" stroke-width="2"/>
</svg>"""
