<!-- Generated: 2026-03-19 | Updated: 2026-03-20 -->

# Digital Finance for Supervision

## Purpose
Conference website and materials for the "Digital Finance for Supervision" hybrid half-day workshop at the European Central Bank (November 30, 2026), organized by the MSCA DIGITAL network (GA 101119635). Speakers present onsite; remote participation via live stream.

## Architecture

Data-driven static site generator. All content lives in `data/*.json`. Generators produce self-contained HTML (base64-embedded images) and LaTeX PDFs. Never edit generated outputs directly.

```
project-root/
├── data/                           # Structured data (source of truth)
│   ├── conference.json             # Master config: dates, venue, branding, funding
│   ├── committee.json              # 10 organizing committee members
│   ├── program.json                # Schedule + call for papers config
│   ├── partners.json               # 19 partner institutions (11 beneficiary + 8 associated)
│   ├── topics.json                 # 3 SupTech research topics
│   └── news.json                   # News/announcement items
├── assets/
│   ├── people/                     # Committee photos (firstname_lastname.jpg/png)
│   └── logos/                      # Institution logos (PNG from Wikimedia Commons)
├── booklet_assets/                 # Venue/Frankfurt photos for print materials
├── scripts/
│   ├── download_photos.py          # Committee photo download utility
│   └── download_all_assets.py      # Logos + venue photos download (Wikimedia API)
├── generate_conference_page.py     # Main website generator → index.html
├── generate_topic_pages.py         # Topic subpage generator → topic_*.html
├── generate_program_pdf.py         # Program PDF wrapper
├── booklet.tex                     # 8-page marketing booklet (LaTeX)
├── poster.tex                      # A0 conference poster (LaTeX)
├── program.tex                     # 1-page program handout (LaTeX)
├── registration.html               # Registration page (hand-crafted)
├── index.html                      # GENERATED - do not edit
├── topic_*.html                    # GENERATED - do not edit
├── booklet.pdf                     # GENERATED
├── poster.pdf                      # GENERATED
└── program.pdf                     # GENERATED
```

## Key Files

| File | Description |
|------|-------------|
| `generate_conference_page.py` | Main generator: reads JSON data, embeds images as base64, produces `index.html` |
| `booklet.tex` | 8-page LaTeX booklet: cover, foreword, about, program, committee, topics, venue, partners |
| `poster.tex` | A0 LaTeX conference poster |
| `program.tex` | 1-page LaTeX program handout |
| `registration.html` | Static registration page (not generated) |
| `CLAUDE.md` | Build commands and project instructions |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `data/` | JSON data files — single source of truth for all content (see `data/AGENTS.md`) |
| `assets/` | People photos and institution logos (see `assets/AGENTS.md`) |
| `booklet_assets/` | Venue and Frankfurt photos for LaTeX materials |
| `scripts/` | Download utilities for photos and logos (see `scripts/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- **Never edit `index.html` or `topic_*.html`** — regenerate via Python scripts
- Edit `data/*.json` files, then run `python generate_conference_page.py`
- For booklet changes, edit `booklet.tex` then compile with `pdflatex` (run twice)
- Partners.json uses `.png` logo filenames (not `.svg`)
- CSS is embedded in `generate_conference_page.py` (not a separate file)

### Build Commands
```bash
python generate_conference_page.py                    # Regenerate website
python generate_topic_pages.py                        # Regenerate topic subpages
pdflatex -interaction=nonstopmode booklet.tex         # Compile booklet (run twice)
python scripts/download_all_assets.py                 # Download logos/venue photos
python scripts/download_photos.py                     # Download committee photos
```

### Deployment
GitHub Pages from `main` branch. After changes:
```bash
git add index.html topic_*.html booklet.pdf
git push origin main
```

### Key Conventions
- Images are base64-embedded in HTML (no external references needed)
- Missing photos/logos show initials-in-circle fallback (deterministic color from name hash)
- ECB branding: `#003399` blue, `#FFD700` gold, `#2E5090` accent
- EU funding acknowledgment required on all outputs (GA 101119635)
- Hybrid format: speakers onsite, remote participation via live stream
- PhD students explicitly invited to contribute

### Current State (2026-03-19)
- Workshop date: November 30, 2026
- 10 committee members (2 missing photos: Mastrokostopoulos, Morin)
- 19 partners, 18 logos downloaded (missing: Cardo AI, Royalton Partners)
- 2 keynotes (30 min each), 8 research talks (4 per session), 1 panel
- CfP deadline: September 15, 2026

## Dependencies

### External (Python)
- Python 3.10+ (standard library only — no pip packages needed)
- `json`, `base64`, `hashlib`, `urllib`, `ssl` — all stdlib

### External (LaTeX)
- pdflatex with packages: tikz, tabularx, booktabs, multicol, qrcode, hyperref, graphicx, fancyhdr

<!-- MANUAL: -->
