# Changelog

All notable changes to the Extended Cyber Kill Chain for AI-Era Threats framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this framework follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (major.minor.patch).

A major version bump indicates a structural change to the stage list or the EKC sub-technique ID scheme. A minor bump indicates new sub-techniques, mapping entries, or case studies. A patch bump indicates editorial corrections.

## [1.0.1] 2026-05-22

Editorial patch release. No changes to the framework itself: no new stages, sub-technique IDs, mappings, or case studies.

### Fixed

- Repo layout: flattened the duplicated `ai-kill-chain/ai-kill-chain/` subdirectory. README relative links (`./examples/...`, `./mappings/...`) now resolve from the repo root. Duplicate `README.md`, `LICENSE`, `CITATION.cff`, `PUBLISH.md`, and the stray top-level `extended-kill-chain.svg` removed. File history preserved via `git mv`.
- `CITATION.cff` placeholder ORCID `0000-0000-0000-0000` corrected to the real ORCID `0009-0008-7320-5927` (matching `.zenodo.json`).

### Added

- Zenodo DOI `10.5281/zenodo.20349357` wired into the README badge, the "Cite as" line, the APA recommended citation, the BibTeX block, and `CITATION.cff` (top-level `doi:` field and an `identifiers:` entry marked as the concept DOI).
- Reverse-direction lookup tables in both mapping files:
  - `mappings/owasp-llm-mapping.md`: per EKC stage, which OWASP categories surface there. Highlights LLM01 spanning Stages 3-6 and LLM06 manifesting only at Stage 7c.
  - `mappings/mitre-atlas-mapping.md`: per ATLAS tactic, which EKC stages and sub-techniques. Notes two structural deltas (ATLAS Persistence splits across EKC Stages 4 and 5; ATLAS Lateral Movement and Privilege Escalation both collapse into EKC Stage 7c).
- `.gitignore` for `.DS_Store` and common editor cruft.

### Notes

- Tag name is `1.0.1` (no `v` prefix) to match the existing `1.0` tag convention.

## [1.0] 2026-05-19

### Added (initial public release)

- Stage 0: Model Supply Chain Compromise (new pre-attack stage) with sub-techniques EKC-0.1 through EKC-0.5.
- AI-augmented sub-techniques inside the original seven stages:
  - Stage 1 (Reconnaissance): EKC-1.1 through EKC-1.5
  - Stage 2 (Weaponization): EKC-2.1 through EKC-2.5
  - Stage 3 (Delivery): EKC-3.1 through EKC-3.6
  - Stage 4 (Exploitation): EKC-4.1 through EKC-4.5
  - Stage 5 (Installation): EKC-5.1 through EKC-5.5
  - Stage 6 (Command and Control): EKC-6.1 through EKC-6.5
- Stage 7 expanded into three sub-stages:
  - 7a: Data Exfiltration (classical)
  - 7b: Model Extraction (new), EKC-7b.1 through EKC-7b.5
  - 7c: Agentic Pivot (new), EKC-7c.1 through EKC-7c.5
- Cross-references to MITRE ATLAS v5.4.0 (February 2026) in `mappings/mitre-atlas-mapping.md`.
- Cross-references to OWASP Top 10 for LLM Applications 2025 in `mappings/owasp-llm-mapping.md`.
- Four worked case studies in `examples/case-studies.md`.
- Mermaid diagram embedded in README. Static SVG version in `diagrams/`.
- CC BY 4.0 license. CITATION.cff for GitHub citation support.

### Verification note

All factual claims in v1.0 were verified against primary sources before release. ATLAS technique IDs and tactic IDs come from the official MITRE atlas-data release notes (https://github.com/mitre-atlas/atlas-data/releases) through v5.4.0. OWASP LLM Top 10 (2025) categories come from genai.owasp.org. Academic citations (Hutchins et al. 2011, Carlini et al. 2021, Tramèr et al. 2016, Greshake et al. 2023, Hubinger et al. 2024) verified against original venues. The framework acknowledges that ATLAS reintroduced Command and Control as a tactic (AML.TA0014) in v4.9.0 (April 2025) and Lateral Movement (AML.TA0015) in v5.1.0 (November 2025). The EKC's value versus ATLAS is the kill-chain-sequenced organization, not the addition of those primitives.

### Notes

- This framework extends the canonical Lockheed Martin Cyber Kill Chain
  (Hutchins, Cloppert, and Amin, 2011) and the operational treatment in
  Nagar and Kumar (2025). It does not replace either.
- DOI will be issued through Zenodo on the first tagged release. The DOI badge in
  README will be updated when issued.
