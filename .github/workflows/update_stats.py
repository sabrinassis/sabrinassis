#!/usr/bin/env python3
"""Calcula XP/nível/conquistas pela API do GitHub e atualiza assets/ficha.svg + README."""
import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FICHA = ROOT / "assets" / "ficha.svg"
START, END = "<!--STATS:START-->", "<!--STATS:END-->"

USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "sabrinassis"

# Atributos da ficha (edite à vontade: valor de 0 a 100)
ATTRS = [
    ("FRONT-END", 80),
    ("BANCO DE DADOS", 60),
    ("CIBERSEGURANÇA", 40),
    ("UX/UI", 80),
    ("COMPORTAMENTO", 100),
]


def gql(query, **variables):
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats-bot"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if "errors" in data:
        sys.exit(f"Erro GraphQL: {data['errors']}")
    return data["data"]


PROFILE_Q = """
query($login:String!){
  user(login:$login){
    createdAt
    followers{totalCount}
    repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){
      totalCount
      nodes{stargazerCount}
    }
  }
}"""

YEAR_Q = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from,to:$to){
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      contributionCalendar{weeks{contributionDays{date contributionCount}}}
    }
  }
}"""


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def collect():
    prof = gql(PROFILE_Q, login=USER)["user"]
    created = datetime.fromisoformat(prof["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    t = dict(commits=0, prs=0, issues=0, reviews=0)
    days = {}
    start = created
    while start < now:
        end = min(start + timedelta(days=364), now)
        c = gql(YEAR_Q, login=USER, **{"from": iso(start), "to": iso(end)})["user"]["contributionsCollection"]
        t["commits"] += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        t["prs"] += c["totalPullRequestContributions"]
        t["issues"] += c["totalIssueContributions"]
        t["reviews"] += c["totalPullRequestReviewContributions"]
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
        start = end + timedelta(seconds=1)

    repos = prof["repositories"]
    t["repos"] = repos["totalCount"]
    t["stars"] = sum(n["stargazerCount"] for n in repos["nodes"])
    t["followers"] = prof["followers"]["totalCount"]
    t["current_streak"], t["longest_streak"] = streaks(days)
    return t


def streaks(days):
    dates = sorted(datetime.fromisoformat(d).date() for d, n in days.items() if n > 0)
    if not dates:
        return 0, 0
    longest = run = 1
    for prev, cur in zip(dates, dates[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        longest = max(longest, run)
    present = set(dates)
    today = datetime.now(timezone.utc).date()
    cursor = today if today in present else today - timedelta(days=1)
    current = 0
    while cursor in present:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def xp_total(t):
    return (t["commits"] * 10 + t["prs"] * 50 + t["issues"] * 20 + t["reviews"] * 30
            + t["stars"] * 25 + t["repos"] * 40 + t["followers"] * 15)


def xp_for_level(level):
    return 50 * (level - 1) ** 2


def level_of(xp):
    return int(math.sqrt(xp / 50)) + 1


def title_of(level):
    if level < 5:
        return "Aprendiz Cafeinada"
    if level < 10:
        return "Dev Cafeinada"
    if level < 20:
        return "Barista do Código"
    if level < 30:
        return "Mestra do Código"
    return "Lenda Cafeinada"


def fmt(n):
    return f"{n:,}".replace(",", ".")


# ---------------- ficha SVG ----------------
FICHA_TPL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 440" width="1200" height="440" role="img" aria-label="Ficha da Desenvolvedora">
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141416"/><stop offset="1" stop-color="#0a0a0b"/></linearGradient>
    <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="#7a5c43"/><stop offset="1" stop-color="#e7dccb"/></linearGradient>
    <linearGradient id="xp" x1="0" x2="1"><stop offset="0" stop-color="#6b5b4b"/><stop offset=".65" stop-color="#c8a27a"/><stop offset="1" stop-color="#f0e6d2"/></linearGradient>
    <linearGradient id="cup" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d2825"/><stop offset="1" stop-color="#161412"/></linearGradient>
    <style>
      .grow{transform-box:fill-box;transform-origin:left center;animation:grow 1.4s ease-out both}
      @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
      .spin{transform-origin:150px 178px;animation:spin 40s linear infinite}
      @keyframes spin{to{transform:rotate(360deg)}}
      .lbl{font-family:'Courier New',monospace;font-size:13px;fill:#7d746a;letter-spacing:2px}
      .val{font-family:'Courier New',monospace;font-size:15px;fill:#ece4d6}
      .att{font-family:'Courier New',monospace;font-size:13px;fill:#bdb3a5;letter-spacing:1px}
      .num{font-family:Georgia,'Times New Roman',serif;font-size:30px;font-weight:bold;fill:#f2ebe0}
      .cap{font-family:'Courier New',monospace;font-size:11px;fill:#7d746a;letter-spacing:2px}
    </style>
  </defs>

  <rect x="2" y="2" width="1196" height="436" rx="14" fill="url(#card)" stroke="#2a2826" stroke-width="2"/>
  <g fill="none" stroke="#c8a27a" stroke-width="3" stroke-linecap="round">
    <path d="M24 56 V24 H56"/><path d="M1144 24 H1176 V56"/>
    <path d="M24 384 V416 H56"/><path d="M1144 416 H1176 V384"/>
  </g>

  <text x="600" y="62" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="24" letter-spacing="9" fill="#e7dccb">FICHA DA DESENVOLVEDORA</text>
  <rect x="470" y="76" width="260" height="2" rx="1" fill="url(#bar)"/>

  <!-- xícara -->
  <circle cx="150" cy="178" r="64" fill="none" stroke="#c8a27a" stroke-width="2"/>
  <g class="spin"><circle cx="150" cy="178" r="76" fill="none" stroke="#6b5b4b" stroke-width="1.2" stroke-dasharray="2 9"/></g>
  <g transform="translate(150,184) scale(.5) translate(-1005,-197)">
    <ellipse cx="990" cy="246" rx="98" ry="11" fill="#1c1917" stroke="#6b5b4b" stroke-width="3"/>
    <path d="M1050 166 H1066 Q1090 166 1090 192 Q1090 218 1062 218 H1046" fill="none" stroke="#e7dccb" stroke-width="10" stroke-linecap="round"/>
    <path d="M930 150 H1050 V190 Q1050 240 1000 240 H980 Q930 240 930 190 Z" fill="url(#cup)" stroke="#e7dccb" stroke-width="4"/>
    <ellipse cx="990" cy="150" rx="60" ry="9" fill="#2a1d14" stroke="#e7dccb" stroke-width="4"/>
    <text x="990" y="208" text-anchor="middle" font-family="'Courier New',monospace" font-size="36" font-weight="bold" fill="#e7dccb">&lt;/&gt;</text>
  </g>

  <!-- campos -->
  <text class="lbl" x="270" y="132">NOME</text>   <text class="val" x="360" y="132">Sabrina Assis</text>
  <text class="lbl" x="270" y="164">CLASSE</text> <text class="val" x="360" y="164">__TITLE__</text>
  <text class="lbl" x="270" y="196">CLÃ</text>    <text class="val" x="360" y="196">ADS (em formação)</text>
  <text class="lbl" x="270" y="228">ORIGEM</text> <text class="val" x="360" y="228">Psicologia → Tecnologia</text>
  <text class="lbl" x="270" y="260">MISSÃO</text> <text class="val" x="360" y="260">Full Stack · Segurança · UX</text>

  <rect x="690" y="108" width="1.5" height="168" fill="#2a2826"/>

  <!-- atributos -->
__ATTRS__

  <!-- estatisticas -->
  <rect x="70" y="302" width="1060" height="1.5" fill="#2a2826"/>
__STATS__

  <!-- XP -->
  <text class="lbl" x="70" y="385" style="fill:#c8a27a">XP · __XP__ / __NEXT__</text>
  <text class="lbl" x="1130" y="385" text-anchor="end" style="fill:#e7dccb">LV __LVL__ · __PCT__%</text>
  <rect x="70" y="395" width="1060" height="14" rx="7" fill="#1e1c1a"/>
  <rect class="grow" x="70" y="395" width="__XPW__" height="14" rx="7" fill="url(#xp)"/>
</svg>"""


def render_ficha(t):
    xp = xp_total(t)
    lvl = level_of(xp)
    cur, nxt = xp_for_level(lvl), xp_for_level(lvl + 1)
    pct = int((xp - cur) / (nxt - cur) * 100)

    attrs = []
    for i, (name, val) in enumerate(ATTRS):
        y = 132 + i * 32
        attrs.append(
            f'  <text class="att" x="720" y="{y}">{name}</text>\n'
            f'  <rect x="880" y="{y - 11}" width="230" height="10" rx="5" fill="#1e1c1a"/>\n'
            f'  <rect class="grow" x="880" y="{y - 11}" width="{230 * val / 100:.0f}" height="10" rx="5" fill="url(#bar)" style="animation-delay:{i * .12:.2f}s"/>\n'
            f'  <text class="att" x="1130" y="{y}" text-anchor="end">{val}</text>'
        )

    items = [("COMMITS", fmt(t["commits"])), ("PULL REQUESTS", fmt(t["prs"])), ("ESTRELAS", fmt(t["stars"])),
             ("REPOSITÓRIOS", fmt(t["repos"])), ("STREAK", f'{t["current_streak"]}d'),
             ("RECORDE", f'{t["longest_streak"]}d')]
    stats = []
    for i, (cap, num) in enumerate(items):
        x = 150 + i * 180
        stats.append(f'  <text class="num" x="{x}" y="342" text-anchor="middle">{num}</text>\n'
                     f'  <text class="cap" x="{x}" y="362" text-anchor="middle">{cap}</text>')

    out = FICHA_TPL
    for k, v in {"__TITLE__": title_of(lvl), "__ATTRS__": "\n".join(attrs), "__STATS__": "\n".join(stats),
                 "__XP__": fmt(xp), "__NEXT__": fmt(nxt), "__LVL__": str(lvl), "__PCT__": str(pct),
                 "__XPW__": f"{1060 * pct / 100:.0f}"}.items():
        out = out.replace(k, v)
    return out


# ---------------- conquistas (markdown) ----------------
ACHIEVEMENTS = [
    ("🐣", "Primeiro Commit", lambda t: t["commits"] >= 1),
    ("💯", "100 Commits", lambda t: t["commits"] >= 100),
    ("🚀", "500 Commits", lambda t: t["commits"] >= 500),
    ("🔥", "Streak de 7 dias", lambda t: t["longest_streak"] >= 7),
    ("⚡", "Streak de 30 dias", lambda t: t["longest_streak"] >= 30),
    ("🤝", "Primeiro Pull Request", lambda t: t["prs"] >= 1),
    ("👀", "Revisora de Código", lambda t: t["reviews"] >= 1),
    ("🐛", "Caçadora de Bugs", lambda t: t["issues"] >= 1),
    ("📦", "Construtora (10 repos)", lambda t: t["repos"] >= 10),
    ("⭐", "Estrelada", lambda t: t["stars"] >= 1),
    ("🌟", "Influente (10 seguidores)", lambda t: t["followers"] >= 10),
    ("🏔️", "Nível 10 alcançado", lambda t: level_of(xp_total(t)) >= 10),
]


def render_achievements(t):
    res = [(i, n, f(t)) for i, n, f in ACHIEVEMENTS]
    done = sum(1 for *_, ok in res if ok)
    cells = [f"{i} **{n}**" if ok else f"🔒 <sub>{n}</sub>" for i, n, ok in res]
    rows = ["| " + " | ".join(cells[k:k + 3]) + " |" for k in range(0, len(cells), 3)]
    now = datetime.now(timezone.utc).strftime("%d/%m/%Y às %H:%M UTC")
    return (f'<div align="center">\n\n#### 🏅 Conquistas ({done}/{len(ACHIEVEMENTS)})\n\n'
            f'| | | |\n| :---: | :---: | :---: |\n' + "\n".join(rows) +
            f'\n\n<sub>🔄 Atualizado em {now}</sub>\n\n</div>')


def main():
    t = collect()
    FICHA.parent.mkdir(exist_ok=True)
    FICHA.write_text(render_ficha(t), encoding="utf-8")

    block = f"{START}\n{render_achievements(t)}\n{END}"
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        sys.exit("Marcadores <!--STATS:START--> / <!--STATS:END--> não encontrados no README.")
    README.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")
    print("Ficha e README atualizados.")


if __name__ == "__main__":
    main()
