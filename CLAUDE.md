# Digital Finance for Supervision

ECB/MSCA DIGITAL Network hybrid half-day workshop, November 30, 2026.

## Build Commands

```bash
# Regenerate website
python generate_conference_page.py

# Generate topic subpages
python generate_topic_pages.py

# Compile LaTeX materials
pdflatex -interaction=nonstopmode booklet.tex && pdflatex -interaction=nonstopmode booklet.tex
pdflatex -interaction=nonstopmode poster.tex && pdflatex -interaction=nonstopmode poster.tex
pdflatex -interaction=nonstopmode program.tex

# Or use the wrapper
python generate_program_pdf.py

# Check for missing committee photos
python scripts/download_photos.py
```

## Data-Driven Architecture

All content lives in `data/*.json`. Edit JSON, then regenerate. Never edit `index.html` directly.

| File | Purpose |
|------|---------|
| `data/conference.json` | Master config: dates, venue, branding, funding |
| `data/committee.json` | 9 organizing committee members |
| `data/program.json` | Schedule + call for papers config |
| `data/partners.json` | 22 DIGITAL network partner institutions |
| `data/topics.json` | 3 SupTech research topics |
| `data/news.json` | News/announcement items |

## Generated Outputs (do not edit)

- `index.html` - Main website (self-contained, base64 images)
- `topic_*.html` - Topic subpages
- `booklet.pdf` - 8-page marketing booklet
- `poster.pdf` - A0 conference poster
- `program.pdf` - 1-page program handout

## Photos

- Committee photos go in `assets/people/` as `firstname_lastname.jpg`
- Logos go in `assets/logos/` as `name.svg`
- Venue photos go in `booklet_assets/`
- Run `python scripts/download_photos.py` to check missing photos

## Deployment

GitHub Pages from `main` branch: https://digital-ai-finance.github.io/digital-finance-supervision/

```bash
python generate_conference_page.py
git add index.html topic_*.html booklet.pdf program.pdf poster.pdf
git commit -m "Update conference materials"
git push
```

## Branding

- Primary: #003399 (ECB blue)
- Secondary: #FFD700 (ECB gold)
- Accent: #2E5090 (DIGITAL network blue)
- Grant: EU Horizon Europe MSCA GA 101119635
