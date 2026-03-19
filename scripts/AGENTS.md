<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-19 -->

# scripts

## Purpose
Utility scripts for downloading and managing image assets from external sources.

## Key Files

| File | Description |
|------|-------------|
| `download_photos.py` | Downloads committee member photos. URLs configured in `PHOTO_URLS` dict. Skips files < 2KB |
| `download_all_assets.py` | Downloads partner logos + venue photos via Wikimedia Commons search API. Uses proper User-Agent |

## For AI Agents

### Working In This Directory
- `download_photos.py`: Add new photo URLs to the `PHOTO_URLS` dict, then run
- `download_all_assets.py`: Add new search terms to `LOGO_SEARCHES` dict for new partners
- Both scripts are idempotent — they skip files that already exist and are > 2KB
- Wikimedia API requires a descriptive User-Agent header (already configured)
- Rate limiting: scripts include `time.sleep()` between API calls

<!-- MANUAL: -->
