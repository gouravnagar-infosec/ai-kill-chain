#!/usr/bin/env python3
"""Refresh the vendored MITRE ATLAS ID index used to validate EKC cross-references.

Usage:
    git clone --depth 1 https://github.com/mitre-atlas/atlas-data
    python tools/refresh_atlas.py atlas-data/dist/v6/ATLAS-2026.10.yaml

Writes data/vendor/atlas-index.json: every ATLAS tactic, technique, case study and
mitigation ID in that release, with its display name and (for techniques) tactics.
Only IDs and names are kept, which is what the build needs to catch typos, renamed
techniques and IDs that ATLAS has retired.
"""
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "vendor" / "atlas-index.json"


def main(path: str) -> None:
    d = yaml.safe_load(open(path, encoding="utf-8"))
    if "collection" not in d:
        sys.exit("Expected ATLAS data format 6.x (a top-level 'collection' key).")

    tactics = d["tactics"]
    techniques = d["techniques"]
    rels = d.get("relationships", {})

    parent = {}
    achieves = {}
    for src, by_type in rels.items():
        for r in by_type.get("specializes", []):
            parent[src] = r["target"]
        for r in by_type.get("achieves", []):
            achieves.setdefault(src, []).append(r["target"])

    def tactic_ids(tid):
        return achieves.get(tid) or achieves.get(parent.get(tid, ""), [])

    entries = {}
    for tid, t in tactics.items():
        entries[tid] = {"type": "tactic", "name": t["name"]}
    for tid, t in techniques.items():
        name = t["name"]
        if tid in parent:
            name = f"{techniques[parent[tid]]['name']}: {name}"
        entries[tid] = {
            "type": "technique",
            "name": name,
            "tactics": sorted(tactic_ids(tid)),
        }
    for cid, c in d.get("case-studies", {}).items():
        entries[cid] = {"type": "case-study", "name": c["name"].rstrip(".")}
    for mid, m in d.get("mitigations", {}).items():
        entries[mid] = {"type": "mitigation", "name": m["name"]}

    out = {
        "source": "https://github.com/mitre-atlas/atlas-data",
        "atlas_version": str(d["collection"]["version"]),
        "data_format": str(d["format-version"]),
        "modified": str(d["collection"].get("modified-date", "")),
        "license_note": "IDs and names from MITRE ATLAS (atlas-data), Copyright 2021-2026 MITRE, Apache License 2.0.",
        "entries": dict(sorted(entries.items())),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"ATLAS {out['atlas_version']}: {len(entries)} IDs written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
