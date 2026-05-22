# Contributing to the Extended Cyber Kill Chain

Thanks for considering a contribution. The framework is maintained as a living artifact because AI-era adversary tradecraft is evolving on a monthly cadence. The framework has to evolve with it.

## What kinds of contributions are welcome

1. **New sub-techniques.** If you observe (or publish on) an AI-era adversary technique that does not fit an existing EKC sub-technique cleanly, open an issue proposing a new ID and a one-paragraph definition.
2. **Case studies.** Real or representative incidents walked through the kill chain, in the format of `examples/case-studies.md`. Public-reporting-based studies are preferred. Anonymized incident write-ups are also welcome.
3. **Mapping refinements.** As MITRE ATLAS, OWASP LLM Top 10, NIST AI RMF, and other frameworks update, the mapping files in `mappings/` need to track. Pull requests against either file are welcome.
4. **Detection signal contributions.** If you operate a SOC or detection-engineering team and have validated a specific detection signal for one of the EKC sub-techniques, contributions to the detection and mitigation section are especially valuable.
5. **Editorial corrections.** Typos, broken links, factual errors.

## What is intentionally out of scope

- Renaming the EKC sub-technique IDs after v1.0. ID stability matters because detection rules and threat reports will start referencing them. Sub-technique IDs added in later versions get new numbers. Existing IDs do not get reassigned.
- Re-numbering the original seven kill-chain stages. The whole value of this framework is preserving the Lockheed Martin spine.
- Replacing the framework with a parallel taxonomy. MITRE ATLAS already exists and is well-maintained. If you want a parallel-taxonomy framework, contribute there.

## How to contribute

1. Open an issue describing the proposed change before sending a pull request, unless it is a trivial editorial fix.
2. For new sub-techniques, propose: (a) the EKC ID, (b) a one-sentence definition, (c) one or two representative observations or references, (d) at least one detection signal, (e) the cross-reference to any matching MITRE ATLAS technique and OWASP LLM Top 10 category.
3. Pull requests should update the relevant section of `README.md`, the mapping files in `mappings/`, and `CHANGELOG.md`.
4. By submitting a contribution, you agree it is released under the same CC BY 4.0 license as the rest of the framework.

## Versioning policy

The framework uses semantic versioning (major.minor.patch).

- Major version bump: structural change to the stage list or the EKC sub-technique ID scheme.
- Minor version bump: new sub-techniques, mapping entries, or case studies.
- Patch version bump: editorial corrections.

A tagged release on GitHub triggers a new Zenodo DOI version. Citations should reference the specific version used.

## Code of conduct

Be substantive, be precise, and assume good faith. Disagree with content, not with people. This is a technical document. The bar for accuracy is high and the bar for politeness is also high.

## Contact

Open an issue, or reach the author through the contact channels listed at https://gouravnagar.com.
