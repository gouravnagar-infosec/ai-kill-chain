# EKC data files

| File | Edit by hand? | Purpose |
|---|---|---|
| `ekc.yaml` | Yes | Source of truth for stages, sub-techniques and cross-references |
| `ekc.json` | No, generated | JSON export for scripts and dashboards |
| `ekc-stix-2.1.json` | No, generated | STIX 2.1 bundle for threat intelligence platforms |
| `stix-ids.json` | No, maintained by the build | Registry that keeps STIX object IDs stable between releases |
| `schema/ekc-source.schema.json` | Yes | JSON Schema for `ekc.yaml` |
| `schema/ekc.schema.json` | Yes | JSON Schema for `ekc.json` (the consumer contract) |
| `schema/stix-extension-ekc.json` | Yes | Schema for the EKC properties on STIX attack-patterns |
| `vendor/atlas-index.json` | No, refreshed by `tools/refresh_atlas.py` | IDs and names from the pinned MITRE ATLAS release |

## Regenerating

```bash
pip install -r tools/requirements.txt
python tools/build.py          # writes the generated files
python tools/build.py --check  # what CI runs: validates and fails on stale output
```

## ekc.json

One object per stage, in kill-chain order. Stage 7 appears as three entries (`7a`, `7b`, `7c`) with `"parent": "7"`. Each sub-technique carries:

- `id`, `name`, `stage`, `added_in`, `description`
- `atlas_techniques` and `atlas_case_studies`: ATLAS ID, current ATLAS name, URL, and (for techniques) the ATLAS tactics
- `owasp_llm_top10_2025` and `owasp_agentic_top10_2026`: ID and title
- for sub-techniques added in v1.1: their own `detection_signals`, `mitigations`, and `references`

Stage-level `detection_signals` and `mitigations` apply to every sub-technique in that stage.

A quick look with `jq`:

```bash
# Every sub-technique tagged with OWASP ASI06 (Memory & Context Poisoning)
jq -r '.stages[].sub_techniques[] | select(any(.owasp_agentic_top10_2026[]; .id=="ASI06")) | "\(.id)  \(.name)"' data/ekc.json

# Which EKC IDs cite a given ATLAS technique
jq -r '.stages[].sub_techniques[] | select(any(.atlas_techniques[]; .id=="AML.T0080.000")) | .id' data/ekc.json
```

## ekc-stix-2.1.json

| STIX object | Count | Notes |
|---|---|---|
| `attack-pattern` | one per EKC ID | `name` is `EKC-x.y: Name`. Stage in `kill_chain_phases` with `kill_chain_name: extended-cyber-kill-chain-ai` and `phase_name` such as `stage-3-delivery` or `stage-7c-agentic-pivot`. External references for the EKC ID, ATLAS, OWASP, and primary sources. |
| `course-of-action` | one per distinct mitigation | Stage-level mitigations are linked to every sub-technique in the stage |
| `relationship` | `mitigates` | course-of-action to attack-pattern |
| `extension-definition` | 1 | Declares the `x_ekc_*` top-level properties. Schema in `schema/stix-extension-ekc.json` |
| `identity`, `marking-definition` | 1 each | Author, and a statement marking with the CC BY 4.0 notice |

Object IDs are random UUIDv4 values, as STIX 2.1 recommends for domain objects, allocated once and recorded in `stix-ids.json` together with the date the object was first published. That date is the object's `created` timestamp and never changes; `modified` moves to each new release date. Re-importing a newer release updates the same objects instead of creating duplicates.

Attack-patterns are keyed by EKC ID, so they are permanent. Courses of action are keyed by the mitigation text, so rewording a mitigation retires the old object and creates a new one. The build prunes retired entries from the registry, and `--check` fails if the registry and the bundle disagree.

The bundle passes the OASIS `stix2-validator` with no errors or warnings (the external-reference hash check is disabled, since the references are documentation links). It loads with the `stix2` Python library, and any platform that imports STIX 2.1 `attack-pattern` objects can ingest it. Kill-chain grouping depends on whether the platform reads `kill_chain_phases` for non-ATT&CK kill chains.

## Refreshing ATLAS

```bash
git clone --depth 1 https://github.com/mitre-atlas/atlas-data /tmp/atlas-data
python tools/refresh_atlas.py /tmp/atlas-data/dist/v6/ATLAS-<version>.yaml
# set reference_versions.mitre_atlas in data/ekc.yaml to the same version
python tools/build.py
```

The build lists every EKC cross-reference that points at an ID the new release no longer has.

## License

EKC data is CC BY 4.0, like the rest of the repository. `vendor/atlas-index.json` holds IDs and names from MITRE ATLAS (atlas-data, Copyright 2021-2026 MITRE, Apache License 2.0). OWASP IDs and titles come from the OWASP GenAI Security Project.
