<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-19 -->

# assets

## Purpose
Image assets for the conference website and materials. Photos and logos are base64-embedded into `index.html` by the generator.

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `people/` | Committee member photos (7 of 10 present). Naming: `firstname_lastname.jpg` or `.png` |
| `logos/` | Partner institution logos (16 of 19 present). Naming: `shortcode.png`. Downloaded from Wikimedia Commons |

## For AI Agents

### Working In This Directory
- Files < 2KB are ignored by the generator (treated as missing/placeholder)
- Missing photos fall back to initials-in-circle with deterministic HSL color from name hash
- After adding/replacing images, run `python generate_conference_page.py` to re-embed them
- Use `python scripts/download_all_assets.py` to batch-download from Wikimedia Commons
- Use `python scripts/download_photos.py` to download committee photos from configured URLs

### Missing Assets
- **People**: `theodoros_mastrokostopoulos.jpg`, `eva_morin.jpg` (both ECB — need internal sourcing)
- **Logos**: `cardo.png` (Cardo AI), `arc.png` (Athena RC), `royalton.png` (Royalton Partners)

<!-- MANUAL: -->
