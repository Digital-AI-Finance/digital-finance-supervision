<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-19 -->

# data

## Purpose
JSON data files — the single source of truth for all conference content. Edit these files, then regenerate outputs. Never edit generated HTML/PDF directly.

## Key Files

| File | Description |
|------|-------------|
| `conference.json` | Master config: dates (Nov 30), venue (ECB Frankfurt), branding colors, funding info, event format (hybrid) |
| `committee.json` | 10 organizing committee members with names, roles, affiliations, photo filenames |
| `program.json` | Schedule (10:00–15:00), session format (4 talks/session), call for papers config and deadlines |
| `partners.json` | 19 institutions: 11 beneficiary + 8 associated. Logo filenames (.png), website URLs, host flags |
| `topics.json` | 3 research topics: AI/ML supervision, NLP regulatory, LLMs in supervision. Each with bullets |
| `news.json` | News items with date, title, content, type (announcement/call/update) |

## For AI Agents

### Working In This Directory
- After editing any JSON file, run `python generate_conference_page.py` to regenerate the website
- After editing `committee.json` or `partners.json`, also update `booklet.tex` manually (not auto-generated from JSON)
- `partners.json` logo filenames must match files in `assets/logos/` (currently `.png` format)
- `committee.json` photo filenames must match files in `assets/people/`
- Dates in `program.json` and `conference.json` must stay in sync

### Validation
- All JSON files must be valid JSON (Python's `json.load()` is the parser)
- Photo/logo files < 2KB are treated as missing by the generator

<!-- MANUAL: -->
