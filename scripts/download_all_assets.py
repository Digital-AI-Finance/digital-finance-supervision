#!/usr/bin/env python3
"""
Download partner logos, venue images using Wikimedia search API + institutional sites.
"""
import json
import ssl
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGOS_DIR = BASE_DIR / "assets" / "logos"
VENUE_DIR = BASE_DIR / "booklet_assets"
PEOPLE_DIR = BASE_DIR / "assets" / "people"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

UA = "DFS2026-Workshop-Bot/1.0 (joerg.osterrieder@utwente.nl) python-urllib"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return r.read()


def wikimedia_search_and_thumb(search_term: str, width: int = 300) -> str | None:
    """Search Wikimedia Commons for a file and return a thumbnail URL."""
    api = "https://commons.wikimedia.org/w/api.php"
    # Search for the file
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "srnamespace": "6",
        "srlimit": "3",
        "format": "json",
    })
    try:
        data = json.loads(fetch(f"{api}?{params}"))
        results = data.get("query", {}).get("search", [])
        if not results:
            return None
        # Get the first result's title
        title = results[0]["title"]
        # Now get the thumbnail
        params2 = urllib.parse.urlencode({
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": width,
            "format": "json",
        })
        time.sleep(0.5)  # Be polite
        data2 = json.loads(fetch(f"{api}?{params2}"))
        pages = data2.get("query", {}).get("pages", {})
        for page in pages.values():
            ii = page.get("imageinfo", [{}])[0]
            return ii.get("thumburl") or ii.get("url")
    except Exception as e:
        print(f"    Search error: {e}")
    return None


def download(url: str, dest: Path, label: str) -> bool:
    if dest.exists() and dest.stat().st_size > 2048:
        print(f"  [SKIP] {label} ({dest.stat().st_size // 1024} KB)")
        return True
    try:
        data = fetch(url)
        if len(data) < 512:
            print(f"  [WARN] {label} - too small ({len(data)} B)")
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"  [OK]   {label} ({len(data) // 1024} KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] {label} - {e}")
        return False


# Search terms for each partner logo
LOGO_SEARCHES = {
    "utwente.png": "University of Twente logo",
    "wu_wien.png": "WU Vienna University Economics logo",
    "unina.png": "University Naples Federico II seal",
    "ase.png": "Bucharest University Economic Studies logo ASE",
    "bbu.png": "Babes-Bolyai University logo",
    "uep.png": "Poznan University Economics Business logo",
    "unipv.png": "University of Pavia logo",
    "unimi.png": "University of Milan Minerva logo",
    "bfh.png": "Berner Fachhochschule logo BFH",
    "ecb.png": "European Central Bank logo ECB",
    "swedbank.png": "Swedbank logo",
    "eit.png": "EIT Digital logo",
}

# Direct institutional URLs as fallbacks
DIRECT_URLS = {
    "ecb.png": "https://www.ecb.europa.eu/shared/img/logo/logo_only.svg",
    "utwente.png": "https://www.utwente.nl/.uc/f3e7e038901028bbe8e0a0c00c0/ut-logo-en.png",
    "swedbank.png": "https://www.swedbank.com/content/dam/swedbank/brand/swedbank-logotype.png",
}

VENUE_SEARCHES = {
    "ecb_tower.jpg": "European Central Bank building Frankfurt Main",
    "frankfurt_skyline.jpg": "Frankfurt am Main skyline",
    "frankfurt_romer.jpg": "Frankfurt Romer Romerberg",
}


def main():
    ok_count = 0
    fail_count = 0

    # First, use already downloaded logos
    already = {"ktu.png", "db.png", "rbi.png", "fraunhofer.png"}

    print("=" * 60)
    print("PARTNER LOGOS - WIKIMEDIA SEARCH")
    print("=" * 60)
    for local_name, search_term in LOGO_SEARCHES.items():
        dest = LOGOS_DIR / local_name
        if dest.exists() and dest.stat().st_size > 2048:
            print(f"  [SKIP] {local_name}")
            ok_count += 1
            continue
        print(f"  Searching: {search_term}")
        url = wikimedia_search_and_thumb(search_term, 300)
        if url:
            if download(url, dest, local_name):
                ok_count += 1
                time.sleep(0.5)
                continue
        # Try direct URL fallback
        if local_name in DIRECT_URLS:
            print(f"  Trying direct URL...")
            if download(DIRECT_URLS[local_name], dest, local_name):
                ok_count += 1
                continue
        fail_count += 1
        time.sleep(0.3)

    for name in already:
        dest = LOGOS_DIR / name
        if dest.exists() and dest.stat().st_size > 512:
            ok_count += 1

    print(f"\nLogos: {ok_count} OK, {fail_count} failed")

    print("\n" + "=" * 60)
    print("VENUE / FRANKFURT PHOTOS")
    print("=" * 60)
    v_ok = 0
    for local_name, search_term in VENUE_SEARCHES.items():
        dest = VENUE_DIR / local_name
        if dest.exists() and dest.stat().st_size > 2048:
            print(f"  [SKIP] {local_name}")
            v_ok += 1
            continue
        print(f"  Searching: {search_term}")
        url = wikimedia_search_and_thumb(search_term, 1280)
        if url:
            if download(url, dest, local_name):
                v_ok += 1
        time.sleep(0.5)

    print(f"\nVenue: {v_ok} downloaded")

    # Final inventory
    print("\n" + "=" * 60)
    print("FINAL INVENTORY")
    print("=" * 60)

    print("\nLogos:")
    if LOGOS_DIR.exists():
        for f in sorted(LOGOS_DIR.iterdir()):
            if f.stat().st_size > 512:
                print(f"  {f.name:30s} {f.stat().st_size:>8,d} bytes")

    print("\nVenue:")
    for f in sorted(VENUE_DIR.iterdir()):
        if f.stat().st_size > 512:
            print(f"  {f.name:30s} {f.stat().st_size:>8,d} bytes")

    print("\nPeople:")
    for f in sorted(PEOPLE_DIR.iterdir()):
        if f.stat().st_size > 512:
            print(f"  {f.name:30s} {f.stat().st_size:>8,d} bytes")

    # Missing
    all_needed = set(LOGO_SEARCHES.keys()) | already | {"cardo.png", "arc.png", "royalton.png"}
    missing = [n for n in sorted(all_needed) if not (LOGOS_DIR / n).exists() or (LOGOS_DIR / n).stat().st_size < 512]
    if missing:
        print(f"\nStill missing logos ({len(missing)}):")
        for m in missing:
            print(f"  {m}")

    missing_p = [n for n in ["theodoros_mastrokostopoulos.jpg", "eva_morin.jpg"]
                 if not (PEOPLE_DIR / n).exists() or (PEOPLE_DIR / n).stat().st_size < 2048]
    if missing_p:
        print(f"\nStill missing people photos ({len(missing_p)}):")
        for m in missing_p:
            print(f"  {m}")


if __name__ == "__main__":
    main()
