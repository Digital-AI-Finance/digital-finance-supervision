#!/usr/bin/env python3
"""
Generate a self-contained conference website (index.html) for the
MSCA DIGITAL Network Workshop "Digital Finance for Supervision" at the ECB.

Reads JSON data from data/ and embeds images as base64.
Falls back to initials circles when photos are missing.

Usage:
    python generate_conference_page.py
"""

import json
import base64
import hashlib
import mimetypes
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
PEOPLE_DIR = ASSETS_DIR / "people"
LOGOS_DIR = ASSETS_DIR / "logos"
OUTPUT_FILE = BASE_DIR / "index.html"

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_json(filename: str, default=None):
    """Load a JSON file from data/, returning *default* if missing."""
    path = DATA_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return default if default is not None else {}


def load_image_base64(path: str) -> str | None:
    """Return a data-URI string for *path*, or None if unusable (<2 KB)."""
    p = Path(path)
    if not p.exists():
        return None
    if p.stat().st_size < 2048:
        return None
    mime, _ = mimetypes.guess_type(str(p))
    if mime is None:
        mime = "image/jpeg"
    with open(p, "rb") as fh:
        encoded = base64.b64encode(fh.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def initials_color(name: str) -> str:
    """Deterministic HSL colour derived from the name hash."""
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    hue = h % 360
    return f"hsl({hue}, 45%, 42%)"


def get_initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[0].upper()

# ---------------------------------------------------------------------------
# Default data (used when JSON files are not yet created)
# ---------------------------------------------------------------------------

DEFAULT_PARTNERS = {
    "beneficiary_partners": [
        {"name": "University of Twente", "short": "UTwente", "country": "Netherlands", "logo": "utwente.png", "is_host": False},
        {"name": "University of Pavia", "short": "UNIPV", "country": "Italy", "logo": "unipv.png", "is_host": False},
        {"name": "Bucharest University of Economic Studies", "short": "ASE", "country": "Romania", "logo": "ase.png", "is_host": False},
        {"name": "Humboldt-Universitaet zu Berlin", "short": "HU Berlin", "country": "Germany", "logo": "hu_berlin.png", "is_host": False},
        {"name": "University of Naples Federico II", "short": "UNINA", "country": "Italy", "logo": "unina.png", "is_host": False},
        {"name": "Babes-Bolyai University", "short": "BBU", "country": "Romania", "logo": "bbu.png", "is_host": False},
        {"name": "University of Milan", "short": "UNIMI", "country": "Italy", "logo": "unimi.png", "is_host": False},
    ],
    "associated_partners": [
        {"name": "European Central Bank", "short": "ECB", "country": "Germany", "logo": "ecb.png", "is_host": True},
        {"name": "ING Bank", "short": "ING", "country": "Netherlands", "logo": "ing.png", "is_host": False},
        {"name": "Prometeia", "short": "Prometeia", "country": "Italy", "logo": "prometeia.png", "is_host": False},
        {"name": "SAS Institute", "short": "SAS", "country": "International", "logo": "sas.png", "is_host": False},
        {"name": "d-fine", "short": "d-fine", "country": "Germany", "logo": "dfine.png", "is_host": False},
        {"name": "Erste Group Bank", "short": "Erste", "country": "Austria", "logo": "erste.png", "is_host": False},
        {"name": "KPMG", "short": "KPMG", "country": "International", "logo": "kpmg.png", "is_host": False},
        {"name": "CaixaBank", "short": "CaixaBank", "country": "Spain", "logo": "caixabank.png", "is_host": False},
        {"name": "National Bank of Romania", "short": "BNR", "country": "Romania", "logo": "bnr.png", "is_host": False},
        {"name": "BitPanda", "short": "BitPanda", "country": "Austria", "logo": "bitpanda.png", "is_host": False},
        {"name": "Banca d'Italia", "short": "BdI", "country": "Italy", "logo": "bdi.png", "is_host": False},
        {"name": "Finanstilsynet (DFSA)", "short": "DFSA", "country": "Denmark", "logo": "dfsa.png", "is_host": False},
        {"name": "Deutsche Bundesbank", "short": "Bundesbank", "country": "Germany", "logo": "bundesbank.png", "is_host": False},
    ],
}

DEFAULT_TOPICS = {
    "topics": [
        {
            "id": "ai-ml",
            "title": "AI/ML for Bank Supervision",
            "icon": "brain",
            "description": "Leveraging artificial intelligence and machine learning techniques to enhance supervisory processes, risk assessment, and early-warning systems for banking oversight.",
            "bullets": [
                "Deep learning for credit risk modeling",
                "Anomaly detection in supervisory data",
                "Explainable AI for regulatory decisions",
                "Predictive analytics for bank distress",
            ],
        },
        {
            "id": "nlp",
            "title": "NLP for Regulatory Reporting",
            "icon": "file-text",
            "description": "Applying natural language processing to automate and improve the analysis of regulatory documents, compliance reports, and supervisory communications.",
            "bullets": [
                "Automated classification of regulatory filings",
                "Sentiment analysis of supervisory correspondence",
                "Information extraction from annual reports",
                "Compliance checking with NLP pipelines",
            ],
        },
        {
            "id": "llm",
            "title": "LLMs in Supervision",
            "icon": "cpu",
            "description": "Exploring the potential and challenges of large language models for supervisory tasks, from document summarization to interactive supervisory assistants.",
            "bullets": [
                "LLM-powered supervisory Q&A systems",
                "Automated report generation and summarization",
                "Fine-tuning LLMs on regulatory corpora",
                "Risk and bias assessment of generative AI in finance",
            ],
        },
    ]
}

# ---------------------------------------------------------------------------
# SVG icons (inline, no external dependencies)
# ---------------------------------------------------------------------------

ICONS = {
    "brain": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><path d="M12 2a5 5 0 0 1 4.77 3.48A4 4 0 0 1 20 9.5a4 4 0 0 1-1.5 3.12A4.5 4.5 0 0 1 17 17.5a4.5 4.5 0 0 1-2.6 1.37A3.5 3.5 0 0 1 12 22a3.5 3.5 0 0 1-2.4-3.13A4.5 4.5 0 0 1 7 17.5a4.5 4.5 0 0 1-1.5-4.88A4 4 0 0 1 4 9.5a4 4 0 0 1 3.23-3.92A5 5 0 0 1 12 2z"/><path d="M12 2v20"/><path d="M8 6h8"/><path d="M7 10h10"/><path d="M8 14h8"/><path d="M9 18h6"/></svg>',
    "file-text": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/><line x1="8" y1="9" x2="10" y2="9"/></svg>',
    "cpu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="48" height="48"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
}

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = r"""
:root {
    --primary: #003399;
    --secondary: #FFD700;
    --accent: #2E5090;
    --dark: #1a1a2e;
    --light: #f5f5f5;
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
    --shadow-lg: 0 8px 30px rgba(0,0,0,.15);
    --radius: 8px;
    --transition: .25s ease;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
    scroll-behavior: smooth;
    font-size: 16px;
}

body {
    font-family: var(--font);
    color: var(--gray-800);
    background: var(--white);
    line-height: 1.65;
}

a { color: var(--primary); text-decoration: none; }
a:hover { color: var(--accent); }

img { max-width: 100%; height: auto; }

section {
    scroll-margin-top: calc(var(--topbar-h) + 24px);
}

/* ---- Sidebar ---- */
.sidebar {
    position: fixed;
    top: 0; left: 0;
    width: var(--sidebar-w);
    height: 100vh;
    background: var(--dark);
    color: var(--gray-200);
    display: flex;
    flex-direction: column;
    z-index: 1000;
    overflow-y: auto;
    border-right: 2px solid var(--secondary);
}

.sidebar-brand {
    padding: 22px 18px 14px;
    font-size: .82rem;
    font-weight: 700;
    letter-spacing: .6px;
    text-transform: uppercase;
    color: var(--secondary);
    border-bottom: 1px solid rgba(255,255,255,.08);
}

.sidebar-nav { list-style: none; padding: 10px 0; flex: 1; }
.sidebar-nav li a {
    display: block;
    padding: 9px 20px;
    font-size: .82rem;
    color: var(--gray-300);
    transition: background var(--transition), color var(--transition), border-left var(--transition);
    border-left: 3px solid transparent;
}
.sidebar-nav li a:hover,
.sidebar-nav li a.active {
    background: rgba(255,215,0,.08);
    color: var(--secondary);
    border-left-color: var(--secondary);
}

.sidebar-footer {
    padding: 14px 18px;
    font-size: .7rem;
    color: var(--gray-600);
    border-top: 1px solid rgba(255,255,255,.06);
}

/* ---- Top bar ---- */
.topbar {
    position: fixed;
    top: 0;
    left: var(--sidebar-w);
    right: 0;
    height: var(--topbar-h);
    background: var(--white);
    border-bottom: 1px solid var(--gray-200);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    z-index: 900;
    box-shadow: var(--shadow-sm);
}

.topbar-title {
    font-size: .92rem;
    font-weight: 600;
    color: var(--primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.btn {
    display: inline-block;
    padding: 9px 22px;
    border-radius: 5px;
    font-weight: 600;
    font-size: .85rem;
    border: none;
    cursor: pointer;
    transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
    text-decoration: none;
}
.btn:hover { transform: translateY(-1px); box-shadow: var(--shadow); }

.btn-gold {
    background: var(--secondary);
    color: var(--dark);
}
.btn-gold:hover { background: #e6c200; color: var(--dark); }

.btn-primary {
    background: var(--primary);
    color: var(--white);
}
.btn-primary:hover { background: var(--accent); color: var(--white); }

.btn-outline {
    background: transparent;
    color: var(--white);
    border: 2px solid var(--secondary);
}
.btn-outline:hover { background: var(--secondary); color: var(--dark); }

/* ---- Main content ---- */
.main-content {
    margin-left: var(--sidebar-w);
    margin-top: 0;
}

.section-padding { padding: 72px 48px; }
.section-alt { background: var(--gray-100); }

.section-header {
    text-align: center;
    margin-bottom: 48px;
}
.section-header h2 {
    font-size: 1.9rem;
    color: var(--primary);
    margin-bottom: 10px;
    position: relative;
    display: inline-block;
}
.section-header h2::after {
    content: '';
    display: block;
    width: 60px;
    height: 3px;
    background: var(--secondary);
    margin: 10px auto 0;
    border-radius: 2px;
}
.section-header p {
    color: var(--gray-600);
    font-size: 1rem;
    max-width: 640px;
    margin: 0 auto;
}

.container { max-width: 1100px; margin: 0 auto; }

/* ---- Hero ---- */
.hero {
    position: relative;
    min-height: 520px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 100px 40px 80px;
    margin-top: var(--topbar-h);
    background: linear-gradient(135deg, var(--primary) 0%, var(--dark) 100%);
    color: var(--white);
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 30% 50%, rgba(46,80,144,.3) 0%, transparent 60%),
                radial-gradient(circle at 80% 30%, rgba(255,215,0,.08) 0%, transparent 50%);
}
.hero-content { position: relative; z-index: 1; max-width: 780px; }
.hero h1 { font-size: 2.7rem; font-weight: 800; line-height: 1.15; margin-bottom: 14px; }
.hero .tagline { font-size: 1.15rem; opacity: .92; margin-bottom: 8px; }
.hero .date-venue {
    font-size: 1rem;
    margin-bottom: 28px;
    opacity: .85;
}
.hero .date-venue strong { color: var(--secondary); }

.countdown {
    display: flex;
    gap: 18px;
    justify-content: center;
    margin-bottom: 32px;
}
.countdown-unit {
    background: rgba(255,255,255,.1);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,215,0,.25);
    border-radius: var(--radius);
    padding: 14px 18px;
    min-width: 78px;
    text-align: center;
}
.countdown-unit .num {
    display: block;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--secondary);
    line-height: 1;
}
.countdown-unit .label {
    display: block;
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
    opacity: .75;
}

.hero-buttons { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }

/* ---- Stats bar ---- */
.stats-bar {
    background: var(--primary);
    color: var(--white);
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    padding: 32px 20px;
}
.stat-item {
    text-align: center;
    padding: 10px 28px;
    min-width: 130px;
}
.stat-num {
    font-size: 2rem;
    font-weight: 800;
    color: var(--secondary);
    line-height: 1;
}
.stat-label {
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-top: 4px;
    opacity: .85;
}

/* ---- About ---- */
.about-text { max-width: 820px; margin: 0 auto; font-size: 1.05rem; line-height: 1.8; color: var(--gray-800); text-align: center; }
.about-text p + p { margin-top: 16px; }

/* ---- Call for papers ---- */
.cfp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; align-items: start; }
.cfp-topics { list-style: none; }
.cfp-topics li {
    padding: 8px 0 8px 28px;
    position: relative;
    font-size: .95rem;
}
.cfp-topics li::before {
    content: '\2713';
    position: absolute;
    left: 0;
    color: var(--secondary);
    font-weight: 700;
}
.cfp-info { background: var(--white); border-radius: var(--radius); padding: 28px; box-shadow: var(--shadow-sm); border-left: 4px solid var(--secondary); }
.cfp-info h3 { color: var(--primary); margin-bottom: 12px; font-size: 1.1rem; }
.cfp-info p { font-size: .92rem; margin-bottom: 10px; }
.cfp-deadline { font-size: 1.15rem; font-weight: 700; color: var(--primary); }

/* ---- Committee ---- */
.committee-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; }
.member-card {
    text-align: center;
    padding: 28px 18px;
    border-radius: var(--radius);
    background: var(--white);
    box-shadow: var(--shadow-sm);
    transition: transform var(--transition), box-shadow var(--transition);
}
.member-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.member-photo {
    width: 100px; height: 100px;
    border-radius: 50%;
    margin: 0 auto 14px;
    object-fit: cover;
    border: 3px solid var(--gray-200);
}
.member-initials {
    width: 100px; height: 100px;
    border-radius: 50%;
    margin: 0 auto 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--white);
    border: 3px solid rgba(255,255,255,.3);
}
.member-name { font-size: 1rem; font-weight: 700; color: var(--gray-800); margin-bottom: 2px; }
.member-role { font-size: .8rem; color: var(--secondary); font-weight: 600; margin-bottom: 4px; text-transform: uppercase; letter-spacing: .4px; }
.member-aff { font-size: .82rem; color: var(--gray-600); }

/* ---- Dates ---- */
.dates-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.date-card {
    text-align: center;
    padding: 28px 16px;
    border-radius: var(--radius);
    background: var(--white);
    box-shadow: var(--shadow-sm);
    border-top: 4px solid var(--primary);
    transition: transform var(--transition), box-shadow var(--transition);
}
.date-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.date-card.highlight { border-top-color: var(--secondary); }
.date-card .dc-icon { font-size: 1.8rem; margin-bottom: 8px; }
.date-card .dc-date { font-size: 1.15rem; font-weight: 700; color: var(--primary); margin-bottom: 6px; }
.date-card .dc-label { font-size: .85rem; color: var(--gray-600); }

/* ---- Program ---- */
.program-table { width: 100%; border-collapse: collapse; background: var(--white); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-sm); }
.program-table th { background: var(--primary); color: var(--white); padding: 14px 18px; text-align: left; font-size: .82rem; text-transform: uppercase; letter-spacing: .5px; }
.program-table td { padding: 14px 18px; border-bottom: 1px solid var(--gray-200); font-size: .92rem; vertical-align: top; }
.program-table tr:last-child td { border-bottom: none; }
.program-table tr:hover td { background: var(--gray-100); }
.type-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: .72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .3px;
}
.type-keynote  { background: var(--secondary); color: var(--dark); }
.type-session  { background: var(--primary); color: var(--white); }
.type-break    { background: var(--gray-200); color: var(--gray-600); }
.type-panel    { background: var(--accent); color: var(--white); }
.type-ceremony { background: var(--dark); color: var(--secondary); }
.program-desc { font-size: .82rem; color: var(--gray-600); margin-top: 4px; }

/* ---- Topics ---- */
.topics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.topic-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 32px 24px;
    box-shadow: var(--shadow-sm);
    transition: transform var(--transition), box-shadow var(--transition);
    border-top: 4px solid var(--primary);
}
.topic-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.topic-icon { color: var(--primary); margin-bottom: 16px; }
.topic-card h3 { color: var(--primary); font-size: 1.1rem; margin-bottom: 10px; }
.topic-card p { font-size: .9rem; color: var(--gray-600); margin-bottom: 14px; }
.topic-bullets { list-style: none; }
.topic-bullets li {
    padding: 4px 0 4px 20px;
    position: relative;
    font-size: .85rem;
    color: var(--gray-800);
}
.topic-bullets li::before {
    content: '';
    position: absolute;
    left: 0; top: 12px;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--secondary);
}

/* ---- Venue ---- */
.venue-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; align-items: start; }
.venue-info h3 { color: var(--primary); margin-bottom: 12px; font-size: 1.15rem; }
.venue-info p { font-size: .92rem; margin-bottom: 12px; color: var(--gray-800); }
.venue-address { background: var(--white); padding: 18px; border-radius: var(--radius); box-shadow: var(--shadow-sm); border-left: 4px solid var(--secondary); margin-bottom: 18px; }
.venue-address strong { color: var(--primary); }
.venue-map { border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); min-height: 320px; }
.venue-map iframe { width: 100%; height: 320px; border: 0; }
.venue-practical { margin-top: 18px; }
.venue-practical h4 { font-size: .95rem; color: var(--accent); margin-bottom: 6px; }
.venue-practical ul { list-style: disc inside; font-size: .88rem; color: var(--gray-600); }
.venue-practical ul li { margin-bottom: 4px; }

/* ---- Partners ---- */
.partners-section-label {
    font-size: 1rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 18px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--gray-200);
}
.partners-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 18px; margin-bottom: 40px; }
.partner-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 20px 14px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform var(--transition), box-shadow var(--transition);
    border: 1px solid var(--gray-200);
}
.partner-card:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.partner-card.host-card { border-color: var(--secondary); border-width: 2px; }
.partner-logo-placeholder {
    width: 70px; height: 70px;
    border-radius: 50%;
    margin: 0 auto 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .85rem;
    font-weight: 700;
    color: var(--white);
}
.partner-logo-img {
    width: 70px; height: 70px;
    border-radius: 50%;
    margin: 0 auto 10px;
    object-fit: contain;
    background: var(--white);
    border: 1px solid var(--gray-200);
}
.partner-name { font-size: .85rem; font-weight: 600; color: var(--gray-800); margin-bottom: 2px; }
.partner-country { font-size: .75rem; color: var(--gray-600); }
.host-badge {
    display: inline-block;
    background: var(--secondary);
    color: var(--dark);
    font-size: .65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: .4px;
}

/* ---- Footer ---- */
.footer {
    background: var(--dark);
    color: var(--gray-300);
    padding: 48px 48px 28px;
}
.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 36px; margin-bottom: 28px; }
.footer h4 { color: var(--secondary); font-size: .9rem; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 12px; }
.footer p, .footer a { font-size: .82rem; color: var(--gray-300); }
.footer a:hover { color: var(--secondary); }
.footer-disclaimer {
    font-size: .75rem;
    color: var(--gray-600);
    border-top: 1px solid rgba(255,255,255,.06);
    padding-top: 18px;
    margin-top: 18px;
    line-height: 1.6;
}
.footer-bottom {
    border-top: 1px solid rgba(255,255,255,.06);
    padding-top: 18px;
    text-align: center;
    font-size: .75rem;
    color: var(--gray-600);
}

/* ---- Responsive ---- */
@media (max-width: 1024px) {
    .committee-grid { grid-template-columns: repeat(2, 1fr); }
    .topics-grid    { grid-template-columns: repeat(2, 1fr); }
    .dates-grid     { grid-template-columns: repeat(2, 1fr); }
    .venue-grid     { grid-template-columns: 1fr; }
    .cfp-grid       { grid-template-columns: 1fr; }
    .footer-grid    { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
    .sidebar { display: none; }
    .topbar { left: 0; }
    .main-content { margin-left: 0; }
    .section-padding { padding: 48px 20px; }
    .hero { padding: 80px 20px 60px; min-height: 420px; }
    .hero h1 { font-size: 1.8rem; }
    .countdown { gap: 10px; }
    .countdown-unit { padding: 10px 12px; min-width: 60px; }
    .countdown-unit .num { font-size: 1.3rem; }
    .committee-grid { grid-template-columns: 1fr; }
    .topics-grid    { grid-template-columns: 1fr; }
    .dates-grid     { grid-template-columns: 1fr 1fr; }
    .stats-bar { gap: 6px; }
    .stat-item { padding: 8px 16px; min-width: 100px; }
    .stat-num { font-size: 1.5rem; }
    .footer { padding: 36px 20px 20px; }
}

@media (max-width: 480px) {
    .dates-grid { grid-template-columns: 1fr; }
    .hero-buttons { flex-direction: column; align-items: center; }
}

/* ---- Booklet banner ---- */
.booklet-banner {
    display: flex; align-items: center; justify-content: center;
    gap: 20px; padding: 16px 20px;
    background: linear-gradient(90deg, #FFD700, #DAA520);
    text-align: center;
}
.booklet-banner span {
    font-size: 1.05rem; font-weight: 700; color: #1a1a2e;
}
.booklet-banner .btn-download {
    display: inline-flex; align-items: center; gap: 8px;
    background: #003399; color: white; padding: 10px 24px;
    border-radius: 6px; text-decoration: none; font-weight: 700;
    transition: background 0.2s;
}
.booklet-banner .btn-download:hover { background: #002266; }

/* ---- News ---- */
.news-list { max-width: 820px; margin: 0 auto; }
.news-item {
    display: flex; gap: 18px; padding: 20px 0;
    border-bottom: 1px solid var(--gray-200);
}
.news-item:last-child { border-bottom: none; }
.news-date-badge {
    flex-shrink: 0; background: var(--primary); color: var(--white);
    padding: 6px 14px; border-radius: 6px; font-size: .78rem;
    font-weight: 700; height: fit-content; white-space: nowrap;
}
.news-body h3 { font-size: 1.05rem; color: var(--gray-800); margin-bottom: 4px; }
.news-body p { font-size: .92rem; color: var(--gray-600); line-height: 1.6; }
.news-type {
    display: inline-block; font-size: .7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .4px; padding: 2px 8px;
    border-radius: 10px; margin-bottom: 6px;
}
.news-type-announcement { background: var(--secondary); color: var(--dark); }
.news-type-call { background: var(--primary); color: var(--white); }
.news-type-update { background: var(--gray-200); color: var(--gray-800); }

/* ---- Print ---- */
@media print {
    .sidebar, .topbar, .countdown, .hero-buttons, .btn { display: none !important; }
    .main-content { margin-left: 0 !important; }
    .hero { min-height: auto; padding: 30px; }
    section { page-break-inside: avoid; }
    .section-padding { padding: 24px 0; }
    body { font-size: 11pt; }
}
"""

# ---------------------------------------------------------------------------
# JavaScript
# ---------------------------------------------------------------------------

JS = r"""
(function(){
    // Countdown to December 3 2026
    var target = new Date('2026-12-03T10:00:00+01:00').getTime();
    function updateCountdown(){
        var now = Date.now();
        var diff = target - now;
        if(diff<=0){
            document.querySelectorAll('.countdown-unit .num').forEach(function(e){e.textContent='0';});
            return;
        }
        var d = Math.floor(diff/86400000);
        var h = Math.floor((diff%86400000)/3600000);
        var m = Math.floor((diff%3600000)/60000);
        var s = Math.floor((diff%60000)/1000);
        var el = document.getElementById('cd-days');   if(el) el.textContent=d;
        el = document.getElementById('cd-hours');  if(el) el.textContent=h;
        el = document.getElementById('cd-mins');   if(el) el.textContent=m;
        el = document.getElementById('cd-secs');   if(el) el.textContent=s;
    }
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // Animated counters
    var observed = false;
    var counters = document.querySelectorAll('.stat-num');
    function animateCounters(){
        if(observed) return;
        observed = true;
        counters.forEach(function(el){
            var text = el.getAttribute('data-target');
            var hasPlus = text.indexOf('+') !== -1;
            var num = parseInt(text.replace('+',''), 10);
            var duration = 1200;
            var start = performance.now();
            function step(ts){
                var progress = Math.min((ts - start) / duration, 1);
                var ease = 1 - Math.pow(1 - progress, 3);
                var current = Math.floor(ease * num);
                el.textContent = current + (hasPlus ? '+' : '');
                if(progress < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
        });
    }
    if('IntersectionObserver' in window){
        var io = new IntersectionObserver(function(entries){
            entries.forEach(function(e){
                if(e.isIntersecting) animateCounters();
            });
        }, {threshold: 0.3});
        var bar = document.querySelector('.stats-bar');
        if(bar) io.observe(bar);
    } else {
        animateCounters();
    }

    // Active sidebar link on scroll
    var sections = document.querySelectorAll('section[id]');
    var navLinks = document.querySelectorAll('.sidebar-nav a');
    function onScroll(){
        var scrollY = window.scrollY + 120;
        var current = '';
        sections.forEach(function(sec){
            if(sec.offsetTop <= scrollY){
                current = sec.getAttribute('id');
            }
        });
        navLinks.forEach(function(a){
            a.classList.remove('active');
            if(a.getAttribute('href') === '#' + current) a.classList.add('active');
        });
    }
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();

    // Smooth scroll for sidebar links (fallback for browsers without CSS smooth)
    navLinks.forEach(function(a){
        a.addEventListener('click', function(ev){
            var id = this.getAttribute('href');
            if(id && id.charAt(0)==='#'){
                var target = document.querySelector(id);
                if(target){
                    ev.preventDefault();
                    target.scrollIntoView({behavior:'smooth'});
                }
            }
        });
    });
})();
"""

# ---------------------------------------------------------------------------
# HTML builders
# ---------------------------------------------------------------------------

def build_head(conf: dict) -> str:
    name = conf.get("name", "Digital Finance for Supervision")
    tagline = conf.get("tagline", "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{name} - {tagline}">
<meta name="keywords" content="digital finance, supervision, ECB, SupTech, AI, machine learning, NLP, MSCA, DIGITAL network">
<meta name="author" content="MSCA DIGITAL Network">
<meta name="theme-color" content="#003399">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{tagline}">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect rx='18' width='100' height='100' fill='%23003399'/><text x='50' y='62' font-size='42' text-anchor='middle' fill='%23FFD700' font-family='sans-serif' font-weight='bold'>DF</text></svg>">
<title>{name}</title>
<style>
{CSS}
</style>
</head>
<body>
"""


def build_sidebar() -> str:
    links = [
        ("hero", "Home"),
        ("about", "About"),
        ("cfp", "Call for Papers"),
        ("committee", "Committee"),
        ("dates", "Key Dates"),
        ("program", "Program"),
        ("topics", "Topics"),
        ("venue", "Venue"),
        ("partners", "Partners"),
        ("news", "News"),
    ]
    items = "\n".join(
        f'<li><a href="#{lid}">{label}</a></li>' for lid, label in links
    )
    return f"""
<nav class="sidebar" aria-label="Main navigation">
  <div class="sidebar-brand">DFS 2026</div>
  <ul class="sidebar-nav">
    {items}
  </ul>
  <div class="sidebar-footer">MSCA DIGITAL Network<br>&copy; 2024 &ndash; 2027</div>
</nav>
"""


def build_topbar(conf: dict) -> str:
    name = conf.get("name", "Digital Finance for Supervision")
    return f"""
<header class="topbar">
  <span class="topbar-title">{name}</span>
  <div style="display:flex;gap:10px;align-items:center;">
    <a href="booklet.pdf" class="btn" style="background:#FFD700;color:#1a1a2e;" download>Download Booklet</a>
    <a href="registration.html" class="btn btn-gold">Register</a>
  </div>
</header>
"""


def build_hero(conf: dict) -> str:
    name = conf.get("name", "Digital Finance for Supervision")
    tagline = conf.get("tagline", "")
    venue = conf.get("venue", {})
    venue_name = venue.get("name", "European Central Bank")
    city = venue.get("city", "Frankfurt am Main")
    return f"""
<section id="hero" class="hero">
  <div class="hero-content">
    <h1>{name}</h1>
    <p class="tagline">{tagline}</p>
    <p class="date-venue"><strong>December 3, 2026</strong> &mdash; {venue_name}, {city}</p>
    <div class="countdown">
      <div class="countdown-unit"><span class="num" id="cd-days">0</span><span class="label">Days</span></div>
      <div class="countdown-unit"><span class="num" id="cd-hours">0</span><span class="label">Hours</span></div>
      <div class="countdown-unit"><span class="num" id="cd-mins">0</span><span class="label">Minutes</span></div>
      <div class="countdown-unit"><span class="num" id="cd-secs">0</span><span class="label">Seconds</span></div>
    </div>
    <div class="hero-buttons">
      <a href="#cfp" class="btn btn-gold">Submit Abstract</a>
      <a href="#program" class="btn btn-outline">View Program</a>
    </div>
  </div>
</section>
"""


def build_booklet_banner() -> str:
    return """
<div class="booklet-banner">
  <span>Download the Workshop Booklet</span>
  <a href="booklet.pdf" class="btn-download" download>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
    Download PDF
  </a>
</div>
"""


def build_news(news_data: list) -> str:
    if not news_data:
        return ""
    items = []
    for n in news_data:
        date = n.get("date", "")
        title = n.get("title", "")
        content = n.get("content", "")
        ntype = n.get("type", "update")
        type_cls = f"news-type-{ntype}"
        items.append(f"""
      <div class="news-item">
        <div class="news-date-badge">{date}</div>
        <div class="news-body">
          <span class="news-type {type_cls}">{ntype}</span>
          <h3>{title}</h3>
          <p>{content}</p>
        </div>
      </div>""")
    return f"""
<section id="news" class="section-padding section-alt">
  <div class="container">
    <div class="section-header">
      <h2>Latest News</h2>
      <p>Stay up to date with workshop announcements and updates.</p>
    </div>
    <div class="news-list">
      {"".join(items)}
    </div>
  </div>
</section>
"""


def build_stats() -> str:
    stats = [
        ("30+", "Participants"),
        ("6", "Research Talks"),
        ("2", "Keynotes"),
        ("1", "Panel Discussion"),
        ("20+", "Partner Institutions"),
    ]
    items = "\n".join(
        f'<div class="stat-item"><span class="stat-num" data-target="{val}">0</span><span class="stat-label">{label}</span></div>'
        for val, label in stats
    )
    return f'<div class="stats-bar">{items}</div>'


def build_about() -> str:
    return """
<section id="about" class="section-padding section-alt">
  <div class="container">
    <div class="section-header">
      <h2>About the Workshop</h2>
    </div>
    <div class="about-text">
      <p>
        <strong>Digital Finance for Supervision</strong> is a half-day workshop organized by the
        MSCA DIGITAL network at the European Central Bank in Frankfurt am Main. The workshop
        brings together leading researchers and practitioners to explore how cutting-edge
        technologies&mdash;artificial intelligence, machine learning, and natural language
        processing&mdash;can transform banking supervision and regulatory processes.
      </p>
      <p>
        The event features two invited keynote presentations, a panel discussion on the role of
        large language models in supervisory processes, and six contributed research talks selected
        through an open call for papers. It offers a unique forum for SupTech innovation,
        bridging the gap between academic research and supervisory practice at one of the world's
        most important financial institutions.
      </p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-top:24px;">
        <div style="background:var(--gray-50,#f8f9fa);border-radius:10px;padding:18px 20px;">
          <h4 style="color:var(--primary);font-size:.95rem;margin-bottom:8px;">Registration</h4>
          <ul style="list-style:disc inside;font-size:.88rem;color:var(--gray-600,#6b7280);">
            <li><strong>Fee:</strong> Free of charge (grant-funded)</li>
            <li><strong>Capacity:</strong> 30&ndash;50 participants</li>
            <li><strong>Deadline:</strong> November 15, 2026</li>
            <li>Registration details will be announced in summer 2026</li>
          </ul>
        </div>
        <div style="background:var(--gray-50,#f8f9fa);border-radius:10px;padding:18px 20px;">
          <h4 style="color:var(--primary);font-size:.95rem;margin-bottom:8px;">Contact &amp; Inquiries</h4>
          <p style="font-size:.88rem;color:var(--gray-600,#6b7280);">
            For questions about submissions, registration, or the workshop, contact the organizing committee:
          </p>
          <p style="margin-top:8px;">
            <a href="mailto:joerg.osterrieder@utwente.nl" style="color:var(--primary);font-weight:600;">joerg.osterrieder@utwente.nl</a>
          </p>
          <p style="margin-top:6px;font-size:.85rem;">
            <a href="https://www.digital-finance-msca.com" target="_blank" rel="noopener" style="color:var(--accent);">DIGITAL Network Website &rarr;</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def build_cfp(program_data: dict) -> str:
    cfp = program_data.get("call_for_papers", {})
    topics = cfp.get("topics", [])
    deadline = cfp.get("deadline", "2026-10-01")
    notification = cfp.get("notification", "")
    camera_ready = cfp.get("camera_ready", "")
    instructions = cfp.get("submission_instructions", "")
    submission_format = cfp.get("submission_format", "")
    review_process = cfp.get("review_process", "")
    submission_email = cfp.get("submission_email", "joerg.osterrieder@utwente.nl")
    topic_items = "\n".join(f"<li>{t}</li>" for t in topics)

    # Build important dates list
    dates_html = f'<li><strong>Submission deadline:</strong> {deadline}</li>'
    if notification:
        dates_html += f'\n            <li><strong>Notification of acceptance:</strong> {notification}</li>'
    if camera_ready:
        dates_html += f'\n            <li><strong>Camera-ready version:</strong> {camera_ready}</li>'

    # Build format/review section
    details_html = ""
    if submission_format:
        details_html += f'<p style="margin-bottom:10px;"><strong>Format:</strong> {submission_format}</p>'
    if review_process:
        details_html += f'<p style="margin-bottom:10px;"><strong>Review:</strong> {review_process}</p>'

    return f"""
<section id="cfp" class="section-padding">
  <div class="container">
    <div class="section-header">
      <h2>Call for Papers</h2>
      <p>We invite submissions on all aspects of digital finance applied to banking supervision.</p>
    </div>
    <div class="cfp-grid">
      <div>
        <h3 style="color:var(--primary);margin-bottom:14px;font-size:1.05rem;">Suggested Topics</h3>
        <ul class="cfp-topics">
          {topic_items}
        </ul>
      </div>
      <div class="cfp-info">
        <h3>Submission Details</h3>
        <p>{instructions}</p>
        {details_html}
        <h4 style="margin-top:16px;color:var(--primary);font-size:.95rem;">Important Dates</h4>
        <ul style="list-style:none;padding:0;margin:8px 0 0 0;font-size:.92rem;">
            {dates_html}
        </ul>
        <p style="margin-top:18px;">
          <a href="mailto:{submission_email}?subject=DFS2026%20Submission" class="btn btn-primary">Submit Abstract</a>
        </p>
      </div>
    </div>
  </div>
</section>
"""


def build_committee(committee_data: dict) -> str:
    members = committee_data.get("organizing_committee", [])
    cards = []
    for m in members:
        name = m.get("name", "")
        role = m.get("role", "")
        aff = m.get("affiliation", "")
        photo_file = m.get("photo", "")
        photo_path = PEOPLE_DIR / photo_file if photo_file else None
        data_uri = load_image_base64(str(photo_path)) if photo_path else None

        if data_uri:
            photo_html = f'<img class="member-photo" src="{data_uri}" alt="{name}">'
        else:
            ini = get_initials(name)
            bg = initials_color(name)
            photo_html = f'<div class="member-initials" style="background:{bg};">{ini}</div>'

        cards.append(f"""
      <div class="member-card">
        {photo_html}
        <div class="member-name">{name}</div>
        <div class="member-role">{role}</div>
        <div class="member-aff">{aff}</div>
      </div>""")

    return f"""
<section id="committee" class="section-padding section-alt">
  <div class="container">
    <div class="section-header">
      <h2>Organizing Committee</h2>
    </div>
    <div class="committee-grid">
      {"".join(cards)}
    </div>
  </div>
</section>
"""


def build_dates() -> str:
    dates = [
        ("\U0001F4E2", "October 1, 2026", "Call for Papers Deadline", False),
        ("\U0001F4E7", "October 15, 2026", "Notification of Acceptance", False),
        ("\U0001F4DD", "November 15, 2026", "Registration Deadline", False),
        ("\U0001F3DB\uFE0F", "December 3, 2026", "Workshop Day", True),
    ]
    cards = []
    for icon, date, label, hl in dates:
        cls = "date-card highlight" if hl else "date-card"
        cards.append(f"""
      <div class="{cls}">
        <div class="dc-icon">{icon}</div>
        <div class="dc-date">{date}</div>
        <div class="dc-label">{label}</div>
      </div>""")
    return f"""
<section id="dates" class="section-padding">
  <div class="container">
    <div class="section-header">
      <h2>Important Dates</h2>
    </div>
    <div class="dates-grid">
      {"".join(cards)}
    </div>
  </div>
</section>
"""


def build_program(program_data: dict) -> str:
    days = program_data.get("days", [])
    rows = []
    for day in days:
        for item in day.get("items", []):
            time = item.get("time", "")
            title = item.get("title", "")
            typ = item.get("type", "session")
            desc = item.get("description", "")
            speaker = item.get("speaker", "")
            badge_cls = f"type-{typ}"
            badge_label = typ.capitalize()

            detail = title
            if speaker and speaker != "TBA":
                detail += f" &mdash; <em>{speaker}</em>"
            elif speaker == "TBA":
                detail += " &mdash; <em>Speaker TBA</em>"
            desc_html = f'<div class="program-desc">{desc}</div>' if desc else ""

            rows.append(f"""
        <tr>
          <td style="white-space:nowrap;font-weight:600;">{time}</td>
          <td>{detail}{desc_html}</td>
          <td><span class="type-badge {badge_cls}">{badge_label}</span></td>
        </tr>""")

    return f"""
<section id="program" class="section-padding section-alt">
  <div class="container">
    <div class="section-header">
      <h2>Program</h2>
      <p>December 3, 2026 &mdash; Half-day workshop (10:00 &ndash; 15:00 CET)</p>
    </div>
    <table class="program-table">
      <thead><tr><th>Time</th><th>Event</th><th>Type</th></tr></thead>
      <tbody>
        {"".join(rows)}
      </tbody>
    </table>
  </div>
</section>
"""


def build_topics(topics_data: dict) -> str:
    topics = topics_data.get("topics", [])
    cards = []
    for t in topics:
        title = t.get("title", "")
        desc = t.get("description", "")
        icon_key = t.get("icon", "brain")
        bullets = t.get("bullets", [])
        icon_svg = ICONS.get(icon_key, ICONS["brain"])
        bullet_items = "\n".join(f"<li>{b}</li>" for b in bullets)
        cards.append(f"""
      <div class="topic-card">
        <div class="topic-icon">{icon_svg}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
        <ul class="topic-bullets">
          {bullet_items}
        </ul>
      </div>""")
    return f"""
<section id="topics" class="section-padding">
  <div class="container">
    <div class="section-header">
      <h2>Research Topics</h2>
      <p>Key research areas for the workshop</p>
    </div>
    <div class="topics-grid">
      {"".join(cards)}
    </div>
  </div>
</section>
"""


def build_venue(conf: dict) -> str:
    venue = conf.get("venue", {})
    address = venue.get("address", "Sonnemannstrasse 20, 60314 Frankfurt am Main")
    return f"""
<section id="venue" class="section-padding section-alt">
  <div class="container">
    <div class="section-header">
      <h2>Venue</h2>
    </div>
    <div class="venue-grid">
      <div class="venue-info">
        <div class="venue-address">
          <strong>European Central Bank</strong><br>
          {address}<br>
          Germany
        </div>
        <p>
          The workshop takes place at the European Central Bank's main building in Frankfurt am Main.
          Opened in 2014, the ECB's iconic twin-tower headquarters on the banks of the River Main
          provides a fitting venue for cutting-edge discussions on supervisory technology and
          digital finance innovation.
        </p>
        <div class="venue-practical">
          <h4>Getting There</h4>
          <ul>
            <li>Frankfurt Airport (FRA) &mdash; 15 min by S-Bahn or taxi</li>
            <li>Frankfurt Hauptbahnhof &mdash; 10 min by tram (Line 11)</li>
            <li>Nearest stop: Ostbahnhof / ECB (tram &amp; bus)</li>
          </ul>
        </div>
        <div class="venue-practical" style="margin-top:14px;">
          <h4>Accommodation</h4>
          <ul>
            <li>Hotels in the Ostend district (walking distance)</li>
            <li>City center hotels (10 min by public transport)</li>
            <li>Frankfurt Hauptbahnhof area (well connected)</li>
          </ul>
        </div>
        <div class="venue-practical" style="margin-top:14px;">
          <h4>ECB Visitor Access</h4>
          <ul>
            <li>All participants must be pre-registered for building access</li>
            <li>Please bring a valid photo ID (passport or national ID card)</li>
            <li>Access details will be sent to registered participants by email</li>
          </ul>
        </div>
        <div class="venue-practical" style="margin-top:14px;">
          <h4>Visa Information</h4>
          <ul>
            <li>EU/EEA citizens: no visa required</li>
            <li>Non-EU participants: check <a href="https://www.auswaertiges-amt.de/en/visa-service" target="_blank" rel="noopener">German visa requirements</a></li>
            <li>Invitation letters for visa purposes available upon request</li>
          </ul>
        </div>
      </div>
      <div class="venue-map">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2558.8!2d8.7017!3d50.1096!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47bd0ea4f1852dc5%3A0xd3d4a5f8e3e5cd56!2sEuropean%20Central%20Bank!5e0!3m2!1sen!2sde!4v1700000000000!5m2!1sen!2sde"
          allowfullscreen loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          title="European Central Bank location">
        </iframe>
      </div>
    </div>
  </div>
</section>
"""


def build_partners(partners_data: dict) -> str:
    beneficiary = partners_data.get("beneficiary_partners", [])
    associated = partners_data.get("associated_partners", [])

    def partner_cards(partners: list) -> str:
        cards = []
        for p in partners:
            name = p.get("name", "")
            short = p.get("short", name)
            country = p.get("country", "")
            is_host = p.get("is_host", False)
            logo_file = p.get("logo", "")
            logo_path = LOGOS_DIR / logo_file if logo_file else None
            data_uri = load_image_base64(str(logo_path)) if logo_path else None

            host_cls = " host-card" if is_host else ""
            host_badge = '<div><span class="host-badge">Host Institution</span></div>' if is_host else ""

            if data_uri:
                img_html = f'<img class="partner-logo-img" src="{data_uri}" alt="{name}">'
            else:
                bg = initials_color(name)
                ini = get_initials(short)
                img_html = f'<div class="partner-logo-placeholder" style="background:{bg};">{ini}</div>'

            cards.append(f"""
        <div class="partner-card{host_cls}">
          {img_html}
          <div class="partner-name">{name}</div>
          <div class="partner-country">{country}</div>
          {host_badge}
        </div>""")
        return "".join(cards)

    return f"""
<section id="partners" class="section-padding">
  <div class="container">
    <div class="section-header">
      <h2>Partner Institutions</h2>
      <p>The MSCA DIGITAL network brings together leading universities, central banks, and industry partners.</p>
    </div>
    <div class="partners-section-label">Associated Partners</div>
    <div class="partners-grid">
      {partner_cards(associated)}
    </div>
    <div class="partners-section-label">Beneficiary Partners</div>
    <div class="partners-grid">
      {partner_cards(beneficiary)}
    </div>
  </div>
</section>
"""


def build_footer(conf: dict) -> str:
    funding = conf.get("funding", [{}])
    ack = funding[0].get("acknowledgment_text", "") if funding else ""
    email = conf.get("contact_email", "joerg.osterrieder@utwente.nl")
    copyright_text = conf.get("copyright", "MSCA DIGITAL Network 2024-2027")
    grant_ref = funding[0].get("grant_ref", "101119635") if funding else "101119635"
    disclaimer = (
        "Funded by the European Union. Views and opinions expressed are however those of the "
        "author(s) only and do not necessarily reflect those of the European Union or the "
        "European Research Executive Agency. Neither the European Union nor the granting "
        "authority can be held responsible for them."
    )
    return f"""
<footer class="footer">
  <div class="main-content" style="margin-left:0;">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4>Funding Acknowledgment</h4>
          <p>{ack}</p>
          <p style="margin-top:8px;">Grant Agreement No. {grant_ref}</p>
        </div>
        <div>
          <h4>Contact</h4>
          <p><a href="mailto:{email}">{email}</a></p>
          <p style="margin-top:8px;"><a href="https://www.digital-finance-msca.com" target="_blank" rel="noopener">DIGITAL Network Website</a></p>
        </div>
        <div>
          <h4>Links</h4>
          <p><a href="https://www.ecb.europa.eu" target="_blank" rel="noopener">European Central Bank</a></p>
          <p><a href="https://marie-sklodowska-curie-actions.ec.europa.eu" target="_blank" rel="noopener">MSCA Programme</a></p>
          <p><a href="https://cordis.europa.eu/project/id/{grant_ref}" target="_blank" rel="noopener">CORDIS Project Page</a></p>
        </div>
      </div>
      <div class="footer-disclaimer">
        {disclaimer}
      </div>
      <div class="footer-bottom">
        &copy; {copyright_text}. All rights reserved.
      </div>
    </div>
  </div>
</footer>
"""


def build_closing() -> str:
    return f"""
<script>
{JS}
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    conf = load_json("conference.json", {})
    committee_data = load_json("committee.json", {"organizing_committee": []})
    program_data = load_json("program.json", {"days": [], "call_for_papers": {}})
    partners_data = load_json("partners.json", DEFAULT_PARTNERS)
    topics_data = load_json("topics.json", DEFAULT_TOPICS)
    news_raw = load_json("news.json", {"news": []})
    news_data = news_raw.get("news", [])

    # If partners.json existed but has no keys we expect, merge defaults
    if not partners_data.get("beneficiary_partners") and not partners_data.get("associated_partners"):
        partners_data = DEFAULT_PARTNERS
    if not topics_data.get("topics"):
        topics_data = DEFAULT_TOPICS

    html_parts = [
        build_head(conf),
        build_sidebar(),
        build_topbar(conf),
        '<div class="main-content">',
        build_hero(conf),
        build_booklet_banner(),
        build_stats(),
        build_about(),
        build_cfp(program_data),
        build_committee(committee_data),
        build_dates(),
        build_program(program_data),
        build_topics(topics_data),
        build_venue(conf),
        build_partners(partners_data),
        build_news(news_data),
        "</div>",
        build_footer(conf),
        build_closing(),
    ]

    html = "\n".join(html_parts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"Generated {OUTPUT_FILE} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
