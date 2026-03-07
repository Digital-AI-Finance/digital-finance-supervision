#!/usr/bin/env python3
"""
Generate individual HTML pages for each research topic.

Reads data/topics.json and data/conference.json, then writes:
  topic_aiml-supervision.html
  topic_nlp-regulatory.html
  topic_llm-supervision.html

Usage:
    python generate_topic_pages.py
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str, default=None):
    path = DATA_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return default if default is not None else {}


SIDEBAR_LINKS = [
    ("index.html#hero", "Home"),
    ("index.html#about", "About"),
    ("index.html#cfp", "Call for Papers"),
    ("index.html#program", "Program"),
    ("index.html#committee", "Committee"),
    ("index.html#topics", "All Topics"),
    ("index.html#venue", "Venue"),
    ("index.html#partners", "Partners"),
]

CSS = """
:root {
    --primary: #003399;
    --secondary: #FFD700;
    --accent: #2E5090;
    --dark: #1a1a2e;
    --white: #ffffff;
    --gray-100: #f8f9fa;
    --gray-200: #e9ecef;
    --gray-300: #dee2e6;
    --gray-600: #6c757d;
    --gray-800: #343a40;
    --sidebar-w: 220px;
    --topbar-h: 56px;
    --font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
    --shadow: 0 4px 12px rgba(0,0,0,.1);
    --radius: 8px;
    --transition: .25s ease;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; }
body { font-family: var(--font); color: var(--gray-800); background: var(--white); line-height: 1.65; }
a { color: var(--primary); text-decoration: none; }
a:hover { color: var(--accent); }

.sidebar {
    position: fixed; top: 0; left: 0; width: var(--sidebar-w); height: 100vh;
    background: var(--dark); color: var(--gray-200); display: flex; flex-direction: column;
    z-index: 1000; overflow-y: auto; border-right: 2px solid var(--secondary);
}
.sidebar-brand {
    padding: 22px 18px 14px; font-size: .82rem; font-weight: 700;
    letter-spacing: .6px; text-transform: uppercase; color: var(--secondary);
    border-bottom: 1px solid rgba(255,255,255,.08);
}
.sidebar-nav { list-style: none; padding: 10px 0; flex: 1; }
.sidebar-nav li a {
    display: block; padding: 9px 20px; font-size: .82rem; color: var(--gray-300);
    transition: background var(--transition), color var(--transition);
    border-left: 3px solid transparent;
}
.sidebar-nav li a:hover { background: rgba(255,215,0,.08); color: var(--secondary); border-left-color: var(--secondary); }
.sidebar-footer {
    padding: 14px 18px; font-size: .7rem; color: var(--gray-600);
    border-top: 1px solid rgba(255,255,255,.06);
}

.topbar {
    position: fixed; top: 0; left: var(--sidebar-w); right: 0; height: var(--topbar-h);
    background: var(--white); border-bottom: 1px solid var(--gray-200);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; z-index: 900; box-shadow: var(--shadow-sm);
}
.topbar-title { font-size: .92rem; font-weight: 600; color: var(--primary); }
.btn {
    display: inline-block; padding: 9px 22px; border-radius: 5px; font-weight: 600;
    font-size: .85rem; text-decoration: none; transition: background var(--transition);
}
.btn-primary { background: var(--primary); color: var(--white); }
.btn-primary:hover { background: var(--accent); color: var(--white); }

.main-content { margin-left: var(--sidebar-w); margin-top: 0; }

.hero {
    position: relative; min-height: 280px; display: flex; align-items: center;
    justify-content: center; text-align: center; padding: 80px 40px 50px;
    margin-top: var(--topbar-h);
    background: linear-gradient(135deg, var(--primary) 0%, var(--dark) 100%);
    color: var(--white);
}
.hero h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 10px; }
.hero p { opacity: .9; font-size: 1.05rem; max-width: 700px; }

.content { padding: 60px 48px; }
.container { max-width: 800px; margin: 0 auto; }

.topic-description {
    font-size: 1.1rem; line-height: 1.8; color: var(--gray-800);
    margin-bottom: 32px; padding: 24px; background: var(--gray-100);
    border-radius: var(--radius); border-left: 4px solid var(--secondary);
}

.bullets-section h2 {
    color: var(--primary); font-size: 1.3rem; margin-bottom: 16px;
}
.bullets-list { list-style: none; margin-bottom: 36px; }
.bullets-list li {
    padding: 10px 0 10px 28px; position: relative;
    font-size: 1rem; border-bottom: 1px solid var(--gray-200);
}
.bullets-list li:last-child { border-bottom: none; }
.bullets-list li::before {
    content: ''; position: absolute; left: 0; top: 18px;
    width: 10px; height: 10px; border-radius: 50%; background: var(--secondary);
}

.cta-box {
    background: var(--primary); color: var(--white); padding: 28px;
    border-radius: var(--radius); text-align: center;
}
.cta-box h3 { font-size: 1.15rem; margin-bottom: 10px; }
.cta-box p { font-size: .92rem; opacity: .9; margin-bottom: 16px; }
.cta-box .btn { background: var(--secondary); color: var(--dark); font-weight: 700; }
.cta-box .btn:hover { background: #e6c200; }

.footer {
    background: var(--dark); color: var(--gray-300); padding: 28px 48px 18px;
}
.footer p { font-size: .78rem; line-height: 1.6; }
.footer .bottom { text-align: center; font-size: .72rem; color: var(--gray-600); margin-top: 12px; }

@media (max-width: 768px) {
    .sidebar { display: none; }
    .topbar { left: 0; }
    .main-content { margin-left: 0; }
    .content { padding: 36px 20px; }
    .hero { padding: 60px 20px 40px; min-height: 220px; }
    .hero h1 { font-size: 1.5rem; }
}
"""


def generate_page(topic: dict, conf: dict) -> str:
    tid = topic["id"]
    title = topic["title"]
    desc = topic["description"]
    bullets = topic.get("bullets", [])
    conf_name = conf.get("name", "Digital Finance for Supervision")

    nav_items = "\n".join(
        f'    <li><a href="{href}">{label}</a></li>' for href, label in SIDEBAR_LINKS
    )
    bullet_items = "\n".join(f"    <li>{b}</li>" for b in bullets)
    funding = conf.get("funding", [{}])
    ack = funding[0].get("acknowledgment_text", "") if funding else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{title} - {conf_name}">
<title>{title} - {conf_name}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect rx='18' width='100' height='100' fill='%23003399'/><text x='50' y='62' font-size='42' text-anchor='middle' fill='%23FFD700' font-family='sans-serif' font-weight='bold'>DF</text></svg>">
<style>
{CSS}
</style>
</head>
<body>

<nav class="sidebar" aria-label="Navigation">
  <div class="sidebar-brand">DFS 2026</div>
  <ul class="sidebar-nav">
{nav_items}
  </ul>
  <div class="sidebar-footer">MSCA DIGITAL Network<br>&copy; 2024 &ndash; 2027</div>
</nav>

<header class="topbar">
  <span class="topbar-title">{conf_name}</span>
  <a href="index.html" class="btn btn-primary">Back to Main Site</a>
</header>

<div class="main-content">
  <section class="hero">
    <div>
      <h1>{title}</h1>
      <p>{desc}</p>
    </div>
  </section>

  <div class="content">
    <div class="container">
      <div class="topic-description">
        {desc}
      </div>

      <div class="bullets-section">
        <h2>Key Research Areas</h2>
        <ul class="bullets-list">
{bullet_items}
        </ul>
      </div>

      <div class="cta-box">
        <h3>Submit Your Research</h3>
        <p>We welcome contributions related to {title.lower()}. Submit an extended abstract by October 1, 2026.</p>
        <a href="index.html#cfp" class="btn">Call for Papers</a>
      </div>
    </div>
  </div>
</div>

<footer class="footer">
  <div style="max-width:800px;margin:0 auto;">
    <p>{ack}</p>
    <div class="bottom">&copy; MSCA DIGITAL Network 2024&ndash;2027. All rights reserved.</div>
  </div>
</footer>

</body>
</html>
"""


def main():
    conf = load_json("conference.json", {})
    topics_data = load_json("topics.json", {"topics": []})
    topics = topics_data.get("topics", [])

    if not topics:
        print("No topics found in data/topics.json")
        return

    for topic in topics:
        tid = topic["id"]
        filename = f"topic_{tid}.html"
        out_path = BASE_DIR / filename
        html = generate_page(topic, conf)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"Generated {out_path}")

    print(f"Done. {len(topics)} topic pages generated.")


if __name__ == "__main__":
    main()
