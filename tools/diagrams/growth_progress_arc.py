def render(params: dict = {}) -> str:
    return """<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Background arc track -->
  <path d="M 170 340 A 240 240 0 0 1 650 340" fill="none" stroke="#e8e4db" stroke-width="20" stroke-linecap="round"/>
  <!-- Gold progress arc (~80% filled) -->
  <path d="M 170 340 A 240 240 0 0 1 624 204" fill="none" stroke="#C9A84C" stroke-width="20" stroke-linecap="round"/>
  <!-- Center stat -->
  <text x="410" y="290" font-size="88" fill="#1A1A2E" font-weight="900" text-anchor="middle">52</text>
  <text x="410" y="340" font-size="26" fill="#666" text-anchor="middle">weeks running</text>
  <!-- Start label -->
  <text x="170" y="378" font-size="18" fill="#aaa" text-anchor="middle">Week 1</text>
  <!-- End label -->
  <text x="650" y="378" font-size="18" fill="#C9A84C" text-anchor="middle" font-weight="700">Week 52</text>
  <!-- Bottom caption -->
  <text x="410" y="430" font-size="20" fill="#666" text-anchor="middle">Built once. Still running.</text>
</svg>"""
