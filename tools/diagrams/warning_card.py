def render(params: dict = {}) -> str:
    return """<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;font-family:Inter,system-ui,sans-serif;">
  <!-- Main card -->
  <rect x="100" y="60" width="620" height="300" rx="12" fill="#1A1A2E"/>
  <!-- Gold triangle warning -->
  <polygon points="410,110 490,240 330,240" fill="none" stroke="#C9A84C" stroke-width="4" stroke-linejoin="round"/>
  <text x="410" y="228" font-size="36" fill="#C9A84C" text-anchor="middle" font-weight="900">!</text>
  <!-- Warning text -->
  <text x="410" y="290" font-size="26" fill="rgba(255,255,255,0.9)" text-anchor="middle" font-weight="700">This will break silently.</text>
  <text x="410" y="328" font-size="20" fill="rgba(255,255,255,0.5)" text-anchor="middle">And you won't notice until it's too late.</text>
  <!-- Bottom caption -->
  <text x="410" y="415" font-size="20" fill="#666" text-anchor="middle">Add the alert before you need it.</text>
</svg>"""
