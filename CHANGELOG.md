# Changelog

All notable changes to the Extended Cyber Kill Chain for AI-Era Threats framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this framework follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (major.minor.patch).

A major version bump indicates a structural change to the stage list or the EKC sub-technique ID scheme. A minor bump indicates new sub-techniques, mapping entries, or case studies. A patch bump indicates editorial corrections.

## [1.1] 2026-11-08

Minor release. No change to the stage list or the EKC ID scheme. All v1.0 IDs keep their meaning; eight IDs are added.

### Added

- Eight agentic sub-techniques inside the existing stages, each with a description, detection signals, mitigations, cross-references, and primary sources (README section "Agentic sub-techniques added in v1.1"):
  - Agent memory poisoning: EKC-3.7 Crafted assistant link delivery; EKC-5.6 Shared agent memory poisoning.
  - Agent-to-agent protocol abuse: EKC-1.6 Peer agent and Agent Card enumeration; EKC-3.8 Malicious or impersonated peer agent; EKC-6.6 Inter-agent session smuggling.
  - Agent credential and token theft: EKC-7c.6 Agent credential and token theft (MCP OAuth tokens, token passthrough, API keys, CI secrets).
  - Computer-use agent attacks: EKC-3.9 Interface-layer injection against computer-use agents; EKC-4.6 Computer-use action hijack.
- `mappings/owasp-agentic-mapping.md`: mapping to the OWASP Top 10 for Agentic Applications (2026), ASI01 to ASI10, with a generated per-ID cross-reference table. Every sub-technique now carries `owasp_agentic` tags.
- Machine-readable export under `data/`, generated from a single source file:
  - `data/ekc.yaml`: source of truth for stages, sub-techniques, and cross-references.
  - `data/ekc.json`: JSON export with ATLAS and OWASP IDs resolved to names and URLs. Schema in `data/schema/ekc.schema.json`.
  - `data/ekc-stix-2.1.json`: STIX 2.1 bundle with 55 attack-patterns (stage in `kill_chain_phases`, kill chain name `extended-cyber-kill-chain-ai`), 46 courses of action, 152 `mitigates` relationships, and an extension-definition for the `x_ekc_*` properties. Object IDs are UUIDv4, registered in `data/stix-ids.json` so they stay stable across releases.
  - `data/vendor/atlas-index.json`: IDs and names from the pinned MITRE ATLAS release, used to validate every cross-reference.
- `tools/build.py` (generate and validate; `--check` for CI), `tools/refresh_atlas.py` (re-pin ATLAS), `tools/validate_sigma.py`, `tools/requirements.txt`, and `.github/workflows/validate.yml`.
- Four 2026 case studies in `examples/case-studies.md`, each reconstructed only from named public sources: AI Recommendation Poisoning (Microsoft, February 2026), PleaseFix (Zenity Labs, March 2026), Claude Code GitHub Action secret exposure (Microsoft, June 2026), and a multi-agent framework used against Taiwanese government systems (Dream Research Labs, August 2026).
- `detections/`: ten example Sigma rules (nine detection rules and one correlation rule) tagged `ekc.<id>`, using generic `ai_agent` and `mcp` log sources with OpenTelemetry GenAI field names where they exist. Clearly labeled as examples.

### Changed

- MITRE ATLAS mapping refreshed from v5.4.0 (February 2026) to v2026.10 (October 28, 2026). The forward and reverse tables in `mappings/mitre-atlas-mapping.md` are now generated from `data/ekc.yaml` and checked against MITRE's release data. Updates for ATLAS changes since v5.4.0:
  - Publish Poisoned AI Agent Tool AML.T0104 is now Publish Poisoned AI Artifacts: AI Agent Tools AML.T0115.002 (ATLAS v2026.07).
  - Infer Training Data Membership AML.T0024.000 is now AML.T0137.000; memorized-data extraction is AML.T0137.003 (ATLAS v2026.10).
  - Renames picked up: Training Data Poisoning (AML.T0020), Supply Chain Compromise and its Software / Data Repository / Model Repository sub-techniques (AML.T0010), Replicate AI Model Behavior (AML.T0005), Enterprise Resource Discovery (AML.T0075), and the AI Attack Adaptation tactic (AML.TA0001).
- README: version 1.1, dates, badges, abstract and relationship sections updated for ATLAS v2026.10 and the OWASP Agentic Top 10; per-stage guidance extended for the new sub-techniques; new "Machine-readable data" section; references added for every new source.
- `mappings/owasp-llm-mapping.md`: LLM Top 10 tags for the eight new IDs.
- `CITATION.cff`, `.zenodo.json`: version 1.1, updated abstract and keywords.
- `CONTRIBUTING.md`: contribution flow now starts at `data/ekc.yaml`; tag naming (`1.1`, no `v`) and export stability rules documented.

### Fixed

Cross-reference errors present in v1.0, found when the mapping was validated against MITRE's ATLAS data:

- AML.T0080.001 was cited as AI Agent Context Poisoning: Memory. Memory is AML.T0080.000; AML.T0080.001 is Thread. Corrected for EKC-4.5, EKC-5.1 and EKC-6.2.
- The LLMjacking case study was cited as AML.CS0029. AML.CS0029 is Google Bard Conversation Exfiltration; LLMjacking is AML.CS0030. Corrected for EKC-7b.5.
- EKC-3.2 cited RAG Credential Harvesting (AML.T0082), a Credential Access technique. Replaced with RAG Poisoning (AML.T0070) and Retrieval Content Crafting (AML.T0066).
- EKC-7c.4 cited AI Agent (AML.T0108), which ATLAS places under Command and Control. Moved to EKC-6.1 and EKC-6.4; EKC-7c.4 now cites LLM Prompt Propagation (AML.T0143).
- The reverse view used the tactic labels "ML Model Access" and "ML Attack Staging". ATLAS v5.4.0 already used AI Model Access and AI Attack Staging.
- Rows that named ATLAS techniques without IDs (Extract ML Model, Create Proxy ML Model, Craft Adversarial Data, Extract Training Data) now carry resolved IDs.

### Verification note

Every new factual claim, ID and date in v1.1 was checked against a primary source before release.

- ATLAS: technique, tactic and case-study IDs, names and tactic assignments come from `mitre-atlas/atlas-data` at the `v6.1.0` tag (content release 2026.10, commit f56c146, October 28, 2026), file `dist/v6/ATLAS-2026.10.yaml`. Release history and renames come from that repository's `CHANGELOG.md` and `dist/manifest.yaml`, which also confirms that legacy v5.4.0 corresponds to content release 2026.02. The build fails if any cited ID is missing from the pinned file.
- OWASP Top 10 for Agentic Applications (2026): IDs, titles, the December 2025 publication date, and the Appendix A cross-map to the LLM Top 10 were read from the official PDF linked at genai.owasp.org. Titles are reproduced exactly, including "Memory & Context Poisoning" and "Unexpected Code Execution (RCE)".
- MCP: token passthrough, confused deputy and scope guidance from the Model Context Protocol specification, version 2025-11-25, "Security Best Practices".
- A2A: Agent Card signing (JWS, RFC 7515, over JCS, RFC 8785), the well-known Agent Card path, and extended-card access control from the A2A specification at the `v1.0.0` tag of `a2aproject/A2A` (tagged March 12, 2026). The project's README states it is a Linux Foundation project contributed by Google.
- Agent session smuggling: Unit 42, Lu and Chen, October 31, 2025. Unit 42 states it found no vulnerability in the A2A protocol itself; EKC-6.6 is described accordingly.
- Case 5: Microsoft Security Blog, February 10, 2026 (50 prompts, 31 companies, 60 days). Case 6: Zenity Labs disclosure, March 3, 2026. Case 7: Microsoft Security Blog, June 5, 2026 (reported April 29, 2026; fixed in Claude Code 2.1.128 on May 5, 2026). Case 8: Dream Research Labs, August 12, 2026 (activity July 1 to 4, 2026), cross-checked against ATLAS AML.CS0071 and AI Incident Database incident 1646. Attribution is reported as Dream's inference only.
- "Agents Rule of Two": Meta, ai.meta.com/blog/practical-ai-agent-security.
- OpenTelemetry GenAI field names used in the Sigma examples come from `open-telemetry/semantic-conventions-genai`, where they are at `development` stability.
- LibreChat advisory GHSA-pmw7-gqwj-f954 (CVE-2026-31951, March 27, 2026) is cited as an example of MCP-related OAuth token exposure.

### Notes

- No Upwind data or incidents are used anywhere. All sources are public.
- Tag name is `1.1` (no `v` prefix), matching `1.0` and `1.0.1`. The Zenodo concept DOI `10.5281/zenodo.20349357` is unchanged; the tag mints a new version DOI under it.

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
