#!/usr/bin/env python3
"""Build and validate every machine-readable EKC artifact from data/ekc.yaml.

    python tools/build.py           # regenerate outputs
    python tools/build.py --check   # fail if anything is invalid or out of date (used in CI)

Outputs
  data/ekc.json                      flat JSON export, ATLAS/OWASP IDs resolved to names
  data/ekc-stix-2.1.json             STIX 2.1 bundle (attack-pattern, course-of-action, relationship)
  mappings/mitre-atlas-mapping.md    tables between the GENERATED markers
  mappings/owasp-agentic-mapping.md  table between the GENERATED markers

Checks
  - data/ekc.yaml against data/schema/ekc-source.schema.json
  - EKC ID format, uniqueness, and that each ID sits in the stage its prefix names
  - every ATLAS technique / case-study ID exists in the vendored ATLAS release
  - sub-techniques added in the current version carry detection signals, mitigations, references
  - README sub-technique tables match the source file name for name
  - data/ekc.json against data/schema/ekc.schema.json
  - the STIX bundle with the OASIS stix2-validator (errors fail the build)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import uuid

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "ekc.yaml"
SRC_SCHEMA = ROOT / "data" / "schema" / "ekc-source.schema.json"
OUT_SCHEMA = ROOT / "data" / "schema" / "ekc.schema.json"
ATLAS_INDEX = ROOT / "data" / "vendor" / "atlas-index.json"
OUT_JSON = ROOT / "data" / "ekc.json"
OUT_STIX = ROOT / "data" / "ekc-stix-2.1.json"
ATLAS_MD = ROOT / "mappings" / "mitre-atlas-mapping.md"
AGENTIC_MD = ROOT / "mappings" / "owasp-agentic-mapping.md"
README = ROOT / "README.md"

ATLAS_URL = "https://atlas.mitre.org"
OWASP_LLM_URL = "https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/"
OWASP_AGENTIC_URL = "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"

OWASP_LLM = {
    "LLM01": "Prompt Injection",
    "LLM02": "Sensitive Information Disclosure",
    "LLM03": "Supply Chain",
    "LLM04": "Data and Model Poisoning",
    "LLM05": "Improper Output Handling",
    "LLM06": "Excessive Agency",
    "LLM07": "System Prompt Leakage",
    "LLM08": "Vector and Embedding Weaknesses",
    "LLM09": "Misinformation",
    "LLM10": "Unbounded Consumption",
}
# Names as printed in the OWASP Top 10 for Agentic Applications (2026), December 2025.
OWASP_AGENTIC = {
    "ASI01": "Agent Goal Hijack",
    "ASI02": "Tool Misuse and Exploitation",
    "ASI03": "Identity and Privilege Abuse",
    "ASI04": "Agentic Supply Chain Vulnerabilities",
    "ASI05": "Unexpected Code Execution (RCE)",
    "ASI06": "Memory & Context Poisoning",
    "ASI07": "Insecure Inter-Agent Communication",
    "ASI08": "Cascading Failures",
    "ASI09": "Human-Agent Trust Exploitation",
    "ASI10": "Rogue Agents",
}
# ATLAS matrix column order.
ATLAS_TACTIC_ORDER = [
    "AML.TA0002", "AML.TA0003", "AML.TA0004", "AML.TA0000", "AML.TA0005", "AML.TA0006",
    "AML.TA0012", "AML.TA0007", "AML.TA0013", "AML.TA0008", "AML.TA0015", "AML.TA0009",
    "AML.TA0001", "AML.TA0014", "AML.TA0010", "AML.TA0011",
]

# STIX IDs are random UUIDv4 values (as STIX 2.1 recommends for SDOs) allocated once and
# kept in this registry together with the date the object was first published, so an
# object keeps the same ID and the same `created` timestamp in every later release.
STIX_IDS = ROOT / "data" / "stix-ids.json"
EXT_SCHEMA_URL = ("https://raw.githubusercontent.com/gouravnagar-infosec/ai-kill-chain/main/"
                  "data/schema/stix-extension-ekc.json")
KILL_CHAIN_NAME = "extended-cyber-kill-chain-ai"
# Publication date of each EKC version. Add the new version here when you release.
RELEASE_DATES = {"1.0": "2026-05-19", "1.0.1": "2026-05-22", "1.1": "2026-11-08"}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


class IdRegistry:
    """Maps a stable object key to {"id": uuid4, "created": first publication date}.

    Keys are derived from content (EKC ID for attack-patterns, mitigation text for
    courses of action). Rewording a mitigation therefore creates a new course-of-action
    and retires the old one; the build prunes registry entries that are no longer emitted.
    """

    def __init__(self, path: pathlib.Path, allocate: bool):
        self.path = path
        self.allocate = allocate
        self.entries: dict = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        self.used: set[str] = set()
        self.added: list[str] = []

    def get(self, kind: str, key: str, first_seen: str) -> tuple[str, str]:
        k = f"{kind}:{key}"
        self.used.add(k)
        if k not in self.entries:
            if not self.allocate:
                fail(f"no STIX ID registered for {k}; run `python tools/build.py`")
                return f"{kind}--00000000-0000-4000-8000-000000000000", ts(first_seen)
            self.entries[k] = {"id": str(uuid.uuid4()), "created": first_seen}
            self.added.append(k)
        e = self.entries[k]
        return f"{kind}--{e['id']}", ts(e["created"])

    def unused(self) -> list[str]:
        return sorted(set(self.entries) - self.used)

    def save(self) -> None:
        stale = self.unused()
        if not self.added and not stale:
            return
        keep = {k: v for k, v in sorted(self.entries.items()) if k in self.used}
        self.path.write_text(json.dumps(keep, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"STIX ID registry: {len(self.added)} added, {len(stale)} retired")


REG: IdRegistry


def stix_id(kind: str, key: str, first_seen: str) -> tuple[str, str]:
    return REG.get(kind, key, first_seen)


def ts(date: str) -> str:
    return f"{date}T00:00:00.000Z"


def phase_name(stage: dict) -> str:
    return f"stage-{stage['id']}-{slug(stage['name'])}"


# --------------------------------------------------------------------------- load + validate

def load_source() -> dict:
    src = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    schema = json.loads(SRC_SCHEMA.read_text(encoding="utf-8"))
    v = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for e in sorted(v.iter_errors(src), key=lambda e: list(e.path)):
        fail(f"ekc.yaml schema: {'/'.join(map(str, e.path))}: {e.message}")
    return src


def validate_semantics(src: dict, atlas: dict) -> None:
    entries = atlas["entries"]
    version = src["framework"]["version"]
    if src["reference_versions"]["mitre_atlas"] != atlas["atlas_version"]:
        fail(f"reference_versions.mitre_atlas is {src['reference_versions']['mitre_atlas']} "
             f"but the vendored ATLAS index is {atlas['atlas_version']}")
    seen = set()
    for st in src["stages"]:
        for t in st["sub_techniques"]:
            tid = t["id"]
            if tid in seen:
                fail(f"duplicate EKC ID {tid}")
            seen.add(tid)
            body = tid[4:]
            expected_stage = body if body == "7a" else body.split(".")[0]
            if expected_stage != st["id"]:
                fail(f"{tid} is listed under stage {st['id']} but its prefix says stage {expected_stage}")
            for a in t.get("atlas", []):
                e = entries.get(a)
                if not e:
                    fail(f"{tid}: ATLAS {a} does not exist in ATLAS {atlas['atlas_version']}")
                elif e["type"] != "technique":
                    fail(f"{tid}: {a} is a {e['type']}, not a technique")
            for c in t.get("atlas_case_studies", []):
                if entries.get(c, {}).get("type") != "case-study":
                    fail(f"{tid}: ATLAS case study {c} does not exist in ATLAS {atlas['atlas_version']}")
            if t["added_in"] == version:
                for k in ("detection_signals", "mitigations", "references"):
                    if not t.get(k):
                        fail(f"{tid} is new in {version} and needs '{k}'")
            if len(t["atlas"]) != len(set(t["atlas"])):
                fail(f"{tid}: duplicate ATLAS IDs")


def validate_readme(src: dict) -> None:
    text = README.read_text(encoding="utf-8")
    rows = dict(re.findall(r"^\| (EKC-[0-9a-c.]+) \| ([^|]+?) \| [^|]+ \|$", text, re.M))
    for st in src["stages"]:
        for t in st["sub_techniques"]:
            if t["id"] == "EKC-7a":
                continue
            if t["id"] not in rows:
                fail(f"README.md has no table row for {t['id']}")
            elif rows[t["id"]].strip() != t["name"]:
                fail(f"README.md names {t['id']} '{rows[t['id']].strip()}' but data/ekc.yaml says '{t['name']}'")
    known = {t["id"] for st in src["stages"] for t in st["sub_techniques"]}
    for rid in rows:
        if rid not in known:
            fail(f"README.md has a row for {rid}, which is not in data/ekc.yaml")


# --------------------------------------------------------------------------- JSON export

def atlas_ref(i: str, entries: dict) -> dict:
    e = entries[i]
    kind = {"technique": "techniques", "case-study": "studies"}[e["type"]]
    out = {"id": i, "name": e["name"], "url": f"{ATLAS_URL}/{kind}/{i}"}
    if e["type"] == "technique":
        out["tactics"] = [{"id": ta, "name": entries[ta]["name"]} for ta in e["tactics"]]
    return out


def build_json(src: dict, atlas: dict) -> dict:
    entries = atlas["entries"]
    fw = src["framework"]
    stages = []
    for st in src["stages"]:
        subs = []
        for t in st["sub_techniques"]:
            row = {
                "id": t["id"],
                "name": t["name"],
                "stage": st["id"],
                "added_in": t["added_in"],
                "description": " ".join(t["description"].split()),
                "atlas_techniques": [atlas_ref(a, entries) for a in t["atlas"]],
                "atlas_case_studies": [atlas_ref(c, entries) for c in t.get("atlas_case_studies", [])],
                "owasp_llm_top10_2025": [{"id": o, "name": OWASP_LLM[o]} for o in t["owasp_llm"]],
                "owasp_agentic_top10_2026": [{"id": o, "name": OWASP_AGENTIC[o]} for o in t["owasp_agentic"]],
            }
            for k in ("detection_signals", "mitigations", "references"):
                if t.get(k):
                    row[k] = [" ".join(x.split()) for x in t[k]]
            subs.append(row)
        s = {
            "id": st["id"],
            "name": st["name"],
            "status": st["status"],
            "summary": " ".join(st["summary"].split()),
            "detection_signals": [" ".join(x.split()) for x in st["detection_signals"]],
            "mitigations": [" ".join(x.split()) for x in st["mitigations"]],
            "sub_techniques": subs,
        }
        if st.get("parent"):
            s["parent"] = st["parent"]
        stages.append(s)
    return {
        "framework": {
            "name": fw["name"],
            "short_name": fw["short_name"],
            "version": fw["version"],
            "release_date": fw["release_date"],
            "author": fw["author"],
            "orcid": fw.get("orcid"),
            "license": fw["license"],
            "doi_concept": fw.get("doi_concept"),
            "repository": fw["repository"],
        },
        "reference_versions": {
            "mitre_atlas": atlas["atlas_version"],
            "mitre_atlas_data_format": atlas["data_format"],
            "owasp_llm_top10": src["reference_versions"]["owasp_llm_top10"],
            "owasp_agentic_top10": src["reference_versions"]["owasp_agentic_top10"],
        },
        "generated_from": "data/ekc.yaml",
        "stages": stages,
    }


# --------------------------------------------------------------------------- STIX 2.1 export

def build_stix(doc: dict) -> dict:
    fw = doc["framework"]
    today = fw["release_date"]
    release = ts(today)
    identity_id, identity_created = stix_id("identity", "gourav-nagar", today)
    marking_id, marking_created = stix_id("marking-definition", "ekc-cc-by-4.0", today)
    readme_url = fw["repository"] + "#stage-by-stage-specification"
    objects = [
        {
            "type": "identity", "spec_version": "2.1", "id": identity_id,
            "created": identity_created, "modified": identity_created,
            "name": fw["author"], "identity_class": "individual",
            "external_references": [{"source_name": "orcid", "url": f"https://orcid.org/{fw['orcid']}"}],
        },
        {
            "type": "marking-definition", "spec_version": "2.1", "id": marking_id,
            "created": marking_created, "created_by_ref": identity_id,
            "definition_type": "statement",
            "definition": {"statement": f"{fw['name']} by {fw['author']}. Licensed CC BY 4.0: "
                                        "https://creativecommons.org/licenses/by/4.0/"},
        },
    ]
    ext_id, ext_created = stix_id("extension-definition", "ekc-properties", today)
    objects.append({
        "type": "extension-definition", "spec_version": "2.1", "id": ext_id,
        "created_by_ref": identity_id, "created": ext_created, "modified": ext_created,
        "name": "EKC attack-pattern properties",
        "description": "Top-level properties carrying the EKC sub-technique ID, stage, version added, and detection signals.",
        "schema": EXT_SCHEMA_URL, "version": "1.0.0",
        "extension_types": ["toplevel-property-extension"],
        "extension_properties": ["x_ekc_id", "x_ekc_stage", "x_ekc_added_in", "x_ekc_detection_signals"],
        "object_marking_refs": [marking_id],
    })
    common = {"created_by_ref": identity_id, "object_marking_refs": [marking_id]}
    created_of: dict[str, str] = {}
    seen: set[str] = set()

    def add_coa(text: str) -> str:
        cid, created = stix_id("course-of-action", text, today)
        created_of[cid] = created
        if cid not in seen:
            seen.add(cid)
            objects.append({
                "type": "course-of-action", "spec_version": "2.1", "id": cid,
                "created": created, "modified": max(created, release),
                "name": text if len(text) <= 120 else text[:117].rsplit(" ", 1)[0] + "...",
                "description": text, **common,
            })
        return cid

    def add_rel(src_id: str, tgt_id: str) -> None:
        first = max(created_of[src_id], created_of[tgt_id])[:10]
        rid, created = stix_id("relationship", f"{src_id}|mitigates|{tgt_id}", first)
        objects.append({
            "type": "relationship", "spec_version": "2.1", "id": rid,
            "created": created, "modified": max(created, release), "relationship_type": "mitigates",
            "source_ref": src_id, "target_ref": tgt_id, **common,
        })

    for st in doc["stages"]:
        phase = phase_name(st)
        stage_coas = [add_coa(m) for m in st["mitigations"]]
        for t in st["sub_techniques"]:
            if t["added_in"] not in RELEASE_DATES:
                fail(f"{t['id']}: add version {t['added_in']} to RELEASE_DATES in tools/build.py")
                continue
            ap_id, created = stix_id("attack-pattern", t["id"], RELEASE_DATES[t["added_in"]])
            created_of[ap_id] = created
            refs = [{"source_name": "ekc", "external_id": t["id"], "url": readme_url}]
            refs += [{"source_name": "mitre-atlas", "external_id": a["id"], "url": a["url"]}
                     for a in t["atlas_techniques"] + t["atlas_case_studies"]]
            refs += [{"source_name": "owasp-llm-top10-2025", "external_id": o["id"], "url": OWASP_LLM_URL}
                     for o in t["owasp_llm_top10_2025"]]
            refs += [{"source_name": "owasp-agentic-top10-2026", "external_id": o["id"], "url": OWASP_AGENTIC_URL}
                     for o in t["owasp_agentic_top10_2026"]]
            refs += [{"source_name": "reference", "url": u} for u in t.get("references", [])]
            ap = {
                "type": "attack-pattern", "spec_version": "2.1", "id": ap_id,
                "created": created, "modified": max(created, release),
                "name": f"{t['id']}: {t['name']}", "description": t["description"],
                "kill_chain_phases": [{"kill_chain_name": KILL_CHAIN_NAME, "phase_name": phase}],
                "external_references": refs,
                "x_ekc_id": t["id"], "x_ekc_stage": st["id"], "x_ekc_added_in": t["added_in"],
                "extensions": {ext_id: {"extension_type": "toplevel-property-extension"}},
                **common,
            }
            if t.get("detection_signals"):
                ap["x_ekc_detection_signals"] = t["detection_signals"]
            objects.append(ap)
            for c in stage_coas:
                add_rel(c, ap_id)
            for m in t.get("mitigations", []):
                add_rel(add_coa(m), ap_id)
    bundle_id, _ = stix_id("bundle", f"ekc-{fw['version']}", today)
    return {"type": "bundle", "id": bundle_id, "objects": objects}


def validate_stix(bundle: dict) -> None:
    try:
        from stix2validator import ValidationOptions, validate_string
    except ImportError:
        fail("stix2-validator is not installed (pip install -r tools/requirements.txt)")
        return
    results = validate_string(json.dumps(bundle), ValidationOptions(version="2.1", strict=False, disabled=["302"]))
    if not isinstance(results, list):
        results = [results]
    for r in results:
        for e in r.errors:
            fail(f"STIX {r.object_id}: {getattr(e, 'message', e)}")
        for w in r.warnings:
            print(f"STIX warning {r.object_id}: {getattr(w, 'message', w)}", file=sys.stderr)
        if not r.is_valid and not r.errors:
            fail("STIX bundle failed validation")


# --------------------------------------------------------------------------- Markdown tables

def replace_block(text: str, label: str, name: str, body: str) -> str:
    start, end = f"<!-- BEGIN GENERATED: {name} -->", f"<!-- END GENERATED: {name} -->"
    if start not in text or end not in text:
        fail(f"{label} is missing the '{name}' GENERATED markers")
        return text
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    note = "<!-- Generated by tools/build.py from data/ekc.yaml. Edit the YAML, not this table. -->"
    return f"{pre}{start}\n{note}\n\n{body.rstrip()}\n\n{end}{post}"


def atlas_forward_table(doc: dict, entries: dict) -> str:
    lines = ["| EKC ID | Sub-technique | ATLAS tactics | ATLAS techniques | ATLAS case studies |", "|---|---|---|---|---|"]
    for st in doc["stages"]:
        for t in st["sub_techniques"]:
            tac_ids = {ta["id"] for a in t["atlas_techniques"] for ta in a["tactics"]}
            tactics = [entries[ta]["name"] for ta in ATLAS_TACTIC_ORDER if ta in tac_ids]
            tech = "; ".join(f"{a['name']} ({a['id']})" for a in t["atlas_techniques"]) or "None"
            cs = "; ".join(c["id"] for c in t["atlas_case_studies"]) or ""
            new = f" (added in {t['added_in']})" if t["added_in"] != "1.0" else ""
            lines.append(f"| {t['id']} | {t['name']}{new} | {'; '.join(tactics)} | {tech} | {cs} |")
    return "\n".join(lines)


def atlas_reverse_table(doc: dict, entries: dict) -> str:
    by_tactic: dict[str, list[tuple[str, str]]] = {ta: [] for ta in ATLAS_TACTIC_ORDER}
    for st in doc["stages"]:
        for t in st["sub_techniques"]:
            for a in t["atlas_techniques"]:
                for ta in a["tactics"]:
                    if (st["id"], t["id"]) not in by_tactic[ta["id"]]:
                        by_tactic[ta["id"]].append((st["id"], t["id"]))
    lines = ["| ATLAS tactic | EKC stages where it surfaces | EKC sub-techniques |", "|---|---|---|"]
    for ta in ATLAS_TACTIC_ORDER:
        hits = by_tactic[ta]
        stages = []
        for s, _ in hits:
            if s not in stages:
                stages.append(s)
        stage_txt = "; ".join(f"Stage {s}" for s in stages) or "None"
        ids = ", ".join(i for _, i in hits) or "None"
        lines.append(f"| {entries[ta]['name']} ({ta}) | {stage_txt} | {ids} |")
    return "\n".join(lines)


def agentic_table(doc: dict) -> str:
    hits: dict[str, list[str]] = {k: [] for k in OWASP_AGENTIC}
    stages: dict[str, list[str]] = {k: [] for k in OWASP_AGENTIC}
    for st in doc["stages"]:
        for t in st["sub_techniques"]:
            for o in t["owasp_agentic_top10_2026"]:
                hits[o["id"]].append(t["id"])
                if st["id"] not in stages[o["id"]]:
                    stages[o["id"]].append(st["id"])
    lines = ["| OWASP ID | Risk | EKC stages | EKC sub-techniques tagged with it |", "|---|---|---|---|"]
    for k, name in OWASP_AGENTIC.items():
        st_txt = ", ".join(stages[k]) or "None"
        lines.append(f"| {k} | {name} | {st_txt} | {', '.join(hits[k]) or 'None'} |")
    return "\n".join(lines)


def readme_added_detail(doc: dict, version: str) -> str:
    """Detail blocks for the sub-techniques added in one version. Each version keeps its
    own README marker (added-in-<version>) so older detail and its anchors never disappear."""
    stage_names = {st["id"]: st["name"] for st in doc["stages"]}
    out = []
    for st in doc["stages"]:
        for t in st["sub_techniques"]:
            if t["added_in"] != version:
                continue
            out.append(f"### {t['id']}. {t['name']}")
            out.append("")
            out.append(f"**Stage {st['id']} ({stage_names[st['id']]}).** {t['description']}")
            out.append("")
            out.append("**Detection signals.**")
            out += [f"- {x}" for x in t["detection_signals"]]
            out.append("")
            out.append("**Mitigations.**")
            out += [f"- {x}" for x in t["mitigations"]]
            out.append("")
            xr = []
            if t["atlas_techniques"]:
                xr.append("ATLAS " + ", ".join(f"[{a['id']}]({a['url']}) {a['name']}" for a in t["atlas_techniques"]))
            if t["atlas_case_studies"]:
                xr.append("ATLAS case studies " + ", ".join(f"[{c['id']}]({c['url']})" for c in t["atlas_case_studies"]))
            if t["owasp_agentic_top10_2026"]:
                xr.append("OWASP Agentic " + ", ".join(f"{o['id']} {o['name']}" for o in t["owasp_agentic_top10_2026"]))
            if t["owasp_llm_top10_2025"]:
                xr.append("OWASP LLM " + ", ".join(f"{o['id']} {o['name']}" for o in t["owasp_llm_top10_2025"]))
            out.append("**Cross-references.** " + ". ".join(xr) + ".")
            out.append("")
            out.append("**Sources.** " + " ".join(f"<{u}>" for u in t["references"]))
            out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- main

def dump(obj: dict) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate and fail if generated files are stale")
    args = ap.parse_args()

    global REG
    REG = IdRegistry(STIX_IDS, allocate=not args.check)
    atlas = json.loads(ATLAS_INDEX.read_text(encoding="utf-8"))
    src = load_source()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    validate_semantics(src, atlas)
    validate_readme(src)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    doc = build_json(src, atlas)
    out_schema = json.loads(OUT_SCHEMA.read_text(encoding="utf-8"))
    for e in jsonschema.Draft202012Validator(out_schema).iter_errors(doc):
        fail(f"ekc.json schema: {'/'.join(map(str, e.path))}: {e.message}")
    bundle = build_stix(doc)
    validate_stix(bundle)

    outputs = {
        OUT_JSON: dump(doc),
        OUT_STIX: dump(bundle),
    }
    atlas_md = ATLAS_MD.read_text(encoding="utf-8")
    atlas_md = replace_block(atlas_md, "mappings/mitre-atlas-mapping.md", "forward", atlas_forward_table(doc, atlas["entries"]))
    atlas_md = replace_block(atlas_md, "mappings/mitre-atlas-mapping.md", "reverse", atlas_reverse_table(doc, atlas["entries"]))
    outputs[ATLAS_MD] = atlas_md
    readme = README.read_text(encoding="utf-8")
    for ver in re.findall(r"<!-- BEGIN GENERATED: added-in-([0-9.]+) -->", readme):
        body = readme_added_detail(doc, ver)
        if not body.strip():
            fail(f"README marker added-in-{ver} has no sub-techniques with added_in {ver}")
        readme = replace_block(readme, "README.md", f"added-in-{ver}", body)
    current = doc["framework"]["version"]
    if any(t["added_in"] == current for st in doc["stages"] for t in st["sub_techniques"]) \
            and f"added-in-{current}" not in readme:
        fail(f"README.md needs a '<!-- BEGIN GENERATED: added-in-{current} -->' block for the new sub-techniques")
    outputs[README] = readme
    outputs[AGENTIC_MD] = replace_block(AGENTIC_MD.read_text(encoding="utf-8"), "mappings/owasp-agentic-mapping.md",
                                        "agentic", agentic_table(doc))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if args.check and REG.unused():
        fail(f"data/stix-ids.json has {len(REG.unused())} entries no longer emitted; run `python tools/build.py`")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    if not args.check:
        REG.save()
    stale = []
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            if args.check:
                stale.append(str(path.relative_to(ROOT)))
            else:
                path.write_text(content, encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print("Out of date, run `python tools/build.py`: " + ", ".join(stale), file=sys.stderr)
        return 1

    n = sum(len(s["sub_techniques"]) for s in doc["stages"])
    kinds: dict[str, int] = {}
    for o in bundle["objects"]:
        kinds[o["type"]] = kinds.get(o["type"], 0) + 1
    print(f"OK: EKC {doc['framework']['version']}, {len(doc['stages'])} stages, {n} sub-techniques, "
          f"ATLAS {atlas['atlas_version']}. STIX objects: {kinds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
