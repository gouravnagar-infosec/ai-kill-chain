# Contributing to the Extended Cyber Kill Chain

Thanks for considering a contribution. The framework is maintained as a living artifact because AI-era adversary tradecraft is evolving on a monthly cadence. The framework has to evolve with it.

## What kinds of contributions are welcome

1. **New sub-techniques.** If you observe (or publish on) an AI-era adversary technique that does not fit an existing EKC sub-technique cleanly, open an issue proposing a new ID and a one-paragraph definition.
2. **Case studies.** Real or representative incidents walked through the kill chain, in the format of `examples/case-studies.md`. Public-reporting-based studies are preferred. Anonymized incident write-ups are also welcome.
3. **Mapping refinements.** As MITRE ATLAS, the OWASP LLM and Agentic Top 10 lists, NIST AI RMF, and other frameworks update, the cross-references need to track. Most of them live in `data/ekc.yaml`; the ATLAS tables are generated from it.
4. **Detection signal contributions.** If you operate a SOC or detection-engineering team and have validated a specific detection signal for one of the EKC sub-techniques, contributions to the detection and mitigation section are especially valuable. So are Sigma rules for `detections/sigma/`, and field mappings from your agent telemetry to the generic `ai_agent` and `mcp` log sources.
5. **Editorial corrections.** Typos, broken links, factual errors.

## What is intentionally out of scope

- Renaming the EKC sub-technique IDs after v1.0. ID stability matters because detection rules and threat reports will start referencing them. Sub-technique IDs added in later versions get new numbers. Existing IDs do not get reassigned.
- Re-numbering the original seven kill-chain stages. The whole value of this framework is preserving the Lockheed Martin spine.
- Replacing the framework with a parallel taxonomy. MITRE ATLAS already exists and is well-maintained. If you want a parallel-taxonomy framework, contribute there.

## How to contribute

1. Open an issue describing the proposed change before sending a pull request, unless it is a trivial editorial fix.
2. For new sub-techniques, propose: (a) the EKC ID, (b) a one-sentence definition, (c) one or two public references, ideally primary sources, (d) at least one detection signal and one mitigation, (e) the cross-reference to any matching MITRE ATLAS technique and OWASP LLM or Agentic Top 10 entry.
3. Edit `data/ekc.yaml` first. It is the source for the JSON and STIX exports, the ATLAS tables, and the "added in this version" section of the README. Then add the row to the stage table in `README.md` and an entry in `CHANGELOG.md`.
4. Run the checks locally. CI runs the same two commands:

   ```bash
   pip install -r tools/requirements.txt
   python tools/build.py          # regenerates outputs and validates everything
   python tools/validate_sigma.py # if you touched detections/
   ```

   Commit the regenerated files. `python tools/build.py --check` fails if they are stale.
5. For Sigma rules: title starts with `EKC Example`, description starts with `EXAMPLE RULE.`, tag with `ekc.<id>`, and cite a public source for the behavior. See `detections/README.md` for the field conventions.
6. By submitting a contribution, you agree it is released under the same CC BY 4.0 license as the rest of the framework.

## Versioning policy

The framework uses semantic versioning (major.minor.patch).

- Major version bump: structural change to the stage list or the EKC sub-technique ID scheme.
- Minor version bump: new sub-techniques, mapping entries, or case studies.
- Patch version bump: editorial corrections.

A tagged release on GitHub triggers a new Zenodo DOI version. Tags use the bare version number (`1.0`, `1.0.1`, `1.1`), not a `v` prefix. Citations should reference the specific version used.

The JSON export (`data/ekc.json`) follows the same rule for its fields: minor releases only add fields. STIX object IDs never change once assigned.

## Code of conduct

Be substantive, be precise, and assume good faith. Disagree with content, not with people. This is a technical document. The bar for accuracy is high and the bar for politeness is also high.

## Contact

Open an issue, or reach the author through the contact channels listed at https://gouravnagar.com.
