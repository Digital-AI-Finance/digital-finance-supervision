#!/usr/bin/env python3
"""
Download committee member photos.

Reads data/committee.json, checks which photos exist in assets/people/,
and downloads any that have URLs configured in PHOTO_URLS below.
Filters out files < 2 KB (placeholder detection).

Usage:
    python scripts/download_photos.py
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PEOPLE_DIR = BASE_DIR / "assets" / "people"

# ---------------------------------------------------------------------------
# Configure photo URLs here. Keys must match the "photo" field in
# committee.json (e.g. "joerg_osterrieder.jpg").
# ---------------------------------------------------------------------------
PHOTO_URLS: dict[str, str] = {
    "joerg_osterrieder.jpg": "https://loop.frontiersin.org/images/profile/587887/203",
    "daniel_pele.jpg": "https://analytics.fabiz.ase.ro/wp-content/uploads/2023/05/Dan-Traian-Pele.jpg",
    "wolfgang_haerdle.png": "https://www.imba.fabiz.ase.ro/wp-content/uploads/2018/09/Wolfgang-Hardle_2-263x263.png",
    "maria_iannario.jpg": "https://loop.frontiersin.org/images/profile/2181453/203",
    "alessandra_tanda.jpg": "https://loop.frontiersin.org/images/profile/669488/203",
    "claudia_tarantola.jpg": "https://cepr.org/sites/default/files/styles/logo/public/profile-photos/236268-claudia_527a13ba45baf3e65044f6cd753c18e8.jpg?itok=ZmfI2aJh",
    "codruta_mare.png": "https://econ.ubbcluj.ro/cv/poze/283_MicrosoftTeams-image-(7).png",
}


def main():
    # Load committee data
    committee_path = DATA_DIR / "committee.json"
    if not committee_path.exists():
        print(f"ERROR: {committee_path} not found.")
        sys.exit(1)

    with open(committee_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    members = data.get("organizing_committee", [])
    if not members:
        print("No committee members found.")
        return

    # Ensure output directory exists
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)

    missing = []
    present = []
    downloaded = []
    skipped_small = []

    for m in members:
        name = m.get("name", "Unknown")
        photo_file = m.get("photo", "")
        if not photo_file:
            missing.append((name, "(no photo field)"))
            continue

        photo_path = PEOPLE_DIR / photo_file

        # Try downloading if URL is configured and file doesn't exist (or is tiny)
        if photo_file in PHOTO_URLS:
            url = PHOTO_URLS[photo_file]
            if not photo_path.exists() or photo_path.stat().st_size < 2048:
                print(f"Downloading {photo_file} for {name}...")
                try:
                    urllib.request.urlretrieve(url, str(photo_path))
                    # Check size after download
                    if photo_path.stat().st_size < 2048:
                        print(f"  WARNING: Downloaded file is < 2 KB (likely a placeholder). Removing.")
                        photo_path.unlink()
                        skipped_small.append((name, photo_file))
                    else:
                        size_kb = photo_path.stat().st_size / 1024
                        print(f"  OK: {size_kb:.1f} KB")
                        downloaded.append((name, photo_file))
                except Exception as e:
                    print(f"  FAILED: {e}")
                    missing.append((name, photo_file))
                continue

        # Check existence
        if photo_path.exists():
            if photo_path.stat().st_size < 2048:
                missing.append((name, f"{photo_file} (< 2 KB placeholder)"))
            else:
                present.append((name, photo_file))
        else:
            missing.append((name, photo_file))

    # Summary
    print("\n" + "=" * 50)
    print("PHOTO STATUS SUMMARY")
    print("=" * 50)

    if present:
        print(f"\nPresent ({len(present)}):")
        for name, f in present:
            print(f"  [OK] {name} -> {f}")

    if downloaded:
        print(f"\nDownloaded ({len(downloaded)}):")
        for name, f in downloaded:
            print(f"  [DL] {name} -> {f}")

    if skipped_small:
        print(f"\nSkipped - too small ({len(skipped_small)}):")
        for name, f in skipped_small:
            print(f"  [--] {name} -> {f}")

    if missing:
        print(f"\nMissing ({len(missing)}):")
        for name, f in missing:
            print(f"  [!!] {name} -> {f}")
        print("\nTo fix, add URLs to the PHOTO_URLS dict in this script.")

    total = len(members)
    ok = len(present) + len(downloaded)
    print(f"\nTotal: {ok}/{total} photos available.")


if __name__ == "__main__":
    main()
