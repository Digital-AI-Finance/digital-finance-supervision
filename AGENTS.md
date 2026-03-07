# AGENTS.md - Digital Finance for Supervision

## Project Overview

Conference website and materials for the "Digital Finance for Supervision" half-day workshop at the European Central Bank (December 3, 2026), organized by the MSCA DIGITAL network (GA 101119635).

## Architecture

Data-driven static site generator. All content stored as JSON, generators produce self-contained HTML and LaTeX PDFs.

```
project-root/
├── data/                           # Structured data (source of truth)
│   ├── conference.json             # Master config
│   ├── committee.json              # 9 organizing committee members
│   ├── program.json                # Schedule + call for papers
│   ├── partners.json               # 22 partner institutions
│   ├── topics.json                 # 3 SupTech research topics
│   └── news.json                   # Announcements
├── assets/
│   ├── people/                     # Committee photos (firstname_lastname.jpg)
│   └── logos/                      # Institution logos (SVG preferred)
├── booklet_assets/                 # Venue photos for print materials
├── scripts/
│   └── download_photos.py          # Photo download utility
├── generate_conference_page.py     # Main website generator → index.html
├── generate_topic_pages.py         # Topic subpage generator → topic_*.html
├── generate_program_pdf.py         # Program PDF wrapper
├── booklet.tex                     # 8-page marketing booklet
├── poster.tex                      # A0 conference poster
├── program.tex                     # 1-page program handout
├── registration.html               # Registration page (hand-crafted)
├── index.html                      # GENERATED - do not edit
├── topic_*.html                    # GENERATED - do not edit
├── booklet.pdf                     # GENERATED
├── poster.pdf                      # GENERATED
└── program.pdf                     # GENERATED
```

## Key Conventions

- Images are base64-embedded in HTML (no external references)
- Missing photos show initials-in-circle fallback
- All generators read from data/*.json
- ECB-led branding: #003399 blue, #FFD700 gold, #2E5090 accent
- EU funding acknowledgment required on all outputs (GA 101119635)

## Modification Workflow

1. Edit the relevant `data/*.json` file
2. Run `python generate_conference_page.py`
3. Run `python generate_topic_pages.py` (if topics changed)
4. Recompile LaTeX if booklet/poster/program changed
5. Commit and push to deploy via GitHub Pages
