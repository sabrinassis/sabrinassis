svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" width="1200" height="320" role="img" aria-label="Sabrina Assis, Café e Código">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0a0a0b"/><stop offset=".6" stop-color="#131214"/><stop offset="1" stop-color="#1c1917"/>
    </linearGradient>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="#c8a27a"/><stop offset="1" stop-color="#4a4038"/>
    </linearGradient>
    <linearGradient id="cup" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2d2825"/><stop offset="1" stop-color="#161412"/>
    </linearGradient>
    <radialGradient id="glow">
      <stop offset="0" stop-color="#c8a27a" stop-opacity=".20"/><stop offset="1" stop-color="#c8a27a" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" opacity=".07"/>
    </pattern>
    <style>
      .st{animation:steam 4.6s ease-in-out infinite}
      @keyframes steam{0%{opacity:0;transform:translateY(12px)}40%{opacity:.75}100%{opacity:0;transform:translateY(-18px)}}
      .ring{transform-origin:990px 170px;animation:spin 60s linear infinite}
      @keyframes spin{to{transform:rotate(360deg)}}
      .pulse{animation:pulse 6s ease-in-out infinite}
      @keyframes pulse{0%,100%{opacity:.7}50%{opacity:1}}
    </style>
  </defs>

  <rect width="1200" height="320" fill="url(#bg)"/>
  <rect width="1200" height="320" fill="url(#dots)"/>

  <!-- xícara -->
  <circle class="pulse" cx="990" cy="170" r="170" fill="url(#glow)"/>
  <g class="ring">
    <circle cx="990" cy="170" r="128" fill="none" stroke="#6b5b4b" stroke-width="1.2" stroke-dasharray="2 12" opacity=".7"/>
    <circle cx="1118" cy="170" r="4" fill="#c8a27a"/>
  </g>
  <path class="st" style="animation-delay:0s"   d="M962 132 q-11 -16 0 -32 q11 -16 0 -32" fill="none" stroke="#bfb2a0" stroke-width="4" stroke-linecap="round"/>
  <path class="st" style="animation-delay:1.4s" d="M990 128 q-11 -16 0 -32 q11 -16 0 -32" fill="none" stroke="#bfb2a0" stroke-width="4" stroke-linecap="round"/>
  <path class="st" style="animation-delay:2.8s" d="M1018 132 q-11 -16 0 -32 q11 -16 0 -32" fill="none" stroke="#bfb2a0" stroke-width="4" stroke-linecap="round"/>

  <ellipse cx="990" cy="246" rx="98" ry="11" fill="#1c1917" stroke="#6b5b4b" stroke-width="2"/>
  <path d="M1050 166 H1066 Q1090 166 1090 192 Q1090 218 1062 218 H1046" fill="none" stroke="#e7dccb" stroke-width="9" stroke-linecap="round"/>
  <path d="M930 150 H1050 V190 Q1050 240 1000 240 H980 Q930 240 930 190 Z" fill="url(#cup)" stroke="#e7dccb" stroke-width="3"/>
  <ellipse cx="990" cy="150" rx="60" ry="9" fill="#2a1d14" stroke="#e7dccb" stroke-width="3"/>
  <text x="990" y="208" text-anchor="middle" font-family="'Courier New', monospace" font-size="36" font-weight="bold" fill="#e7dccb">&lt;/&gt;</text>

  <!-- texto -->
  <text x="70" y="96" font-family="'Courier New', monospace" font-size="15" fill="#8a7d6e">$ brew install ideias &amp;&amp; git push</text>
  <text x="70" y="172" font-family="Georgia, 'Times New Roman', serif" font-size="62" font-weight="bold" letter-spacing="5" fill="#f2ebe0">SABRINA ASSIS</text>
  <rect x="70" y="190" width="540" height="3" rx="1.5" fill="url(#line)"/>
  <text x="70" y="232" font-family="'Courier New', monospace" font-size="17" letter-spacing="6" fill="#a89a88">CAF&#201; &amp; C&#211;DIGO &#183; ADS</text>
</svg>'''
open("assets/hero.svg", "w", encoding="utf-8").write(svg)
print("hero ok")
