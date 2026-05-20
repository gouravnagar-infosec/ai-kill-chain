# Publishing checklist

For the author's reference, not part of the framework itself. Delete this file before public release if preferred, or keep it as `PUBLISH.md` in the repo.

Goal: turn this folder into a citable, dated, DOI-bearing public artifact. Order matters. DOI assignment depends on a tagged GitHub release.

## 1. Push to GitHub (5 minutes)

```bash
# from the repo root
git init
git add .
git commit -m "Initial release v1.0. Extended Cyber Kill Chain for AI-Era Threats"
git branch -M main
git remote add origin https://github.com/gouravnagar-infosec/ai-kill-chain.git
git push -u origin main
```

In the repo's About section on GitHub, set:

- Description: A defender-side framework that extends the Lockheed Martin Cyber Kill Chain with AI-era stages: model supply chain compromise, prompt injection delivery, agentic pivot, model extraction.
- Website: https://gouravnagar.com (or a dedicated landing page if you make one).
- Topics: `cybersecurity`, `ai-security`, `kill-chain`, `prompt-injection`, `llm-security`, `threat-modeling`, `mitre-atlas`, `owasp-llm-top10`, `detection-engineering`, `agentic-ai`.

The `CITATION.cff` file is already in place, so GitHub will display a "Cite this repository" button on the repo home page.

## 2. Register a Zenodo DOI (15 minutes, one-time setup)

This is what makes the artifact citable in the way academic-style citations expect. A persistent identifier that survives URL changes.

1. Sign in to https://zenodo.org with your GitHub account.
2. Go to Account, then GitHub, and toggle the `gouravnagar-infosec/ai-kill-chain` repo to ON.
3. Back in GitHub, create a tagged release.
   - Go to the repo, then Releases, then Draft a new release.
   - Tag: `v1.0`
   - Title: `v1.0. Extended Cyber Kill Chain for AI-Era Threats`
   - Description: paste the v1.0 section of `CHANGELOG.md`.
   - Click Publish release.
4. Zenodo will detect the release within a few minutes and mint a DOI. Find it at https://zenodo.org/account/settings/github/.
5. Update the DOI badge in `README.md`.
   - Replace `pending-zenodo` with the actual Zenodo DOI string.
   - Add a citation line under the title that includes the DOI.
6. Later tagged releases (`v1.1`, `v2.0`) get their own DOIs automatically. A "concept DOI" always points to the latest version. Specific-version DOIs are immutable.

## 3. Optional but high-leverage: submit as a preprint

This is what gets the framework into search results and academic citation tools.

**SSRN** (easier, no review, accepts security and policy work):

- Create an SSRN author account if you don't have one.
- Convert `README.md` to a PDF, or use the README content as the body of a paper-format submission.
- Submit to a relevant SSRN network. *Cybersecurity, Privacy and Networks* is the right primary network. *Information Systems and eBusiness* is a relevant secondary.
- Title: *Extended Cyber Kill Chain for AI-Era Threats: A Defender-Side Framework Integrating Model Supply Chain Compromise, Prompt Injection, Model Extraction, and Agentic Pivot Into the Lockheed Martin Kill Chain*.
- Use the README abstract.
- Include the GitHub URL and Zenodo DOI in the SSRN submission's "additional information" field.

**arXiv** (more rigorous, requires endorsement for first submission to `cs.CR`):

- The cs.CR (Cryptography and Security) category is the right home.
- arXiv prefers LaTeX for clean submissions. Let me know if you want a `paper.tex` version generated and I'll produce one in a follow-up.
- Endorsement: if you don't have one yet, ask a colleague who has previously submitted to cs.CR.

## 4. Build outbound visibility

Once the GitHub repo and the Zenodo DOI are live, the highest-leverage next moves:

- LinkedIn announcement post. Frame it as the public companion to the book, with a specific call-out to where the framework genuinely extends prior art (kill-chain-sequenced view, single Stage 0 for supply chain, Stage 7 split into three peer sub-stages). One concrete claim per paragraph. Link to the repo.
- Blog post on gouravnagar.com. A longer-form walkthrough with the diagram embedded and one of the case studies expanded. Cross-link to the repo and to the book.
- Submit to a conference CFP that aligns with your speaking calendar. RSA, Black Hat, BSides, SANS HackFest, AI Village. The framework gives you a fresh, dated artifact to anchor a talk proposal around.
- Direct outreach to maintainers of adjacent frameworks. The MITRE ATLAS team accepts community contributions. OWASP LLM Top 10 has a working group. If your sub-techniques get cited in either, that's a strong impact signal.

## 5. Citation impact tracking

For the citation case, set up tracking once published:

- Google Scholar. Search for the title quarterly. Set up an alert.
- Semantic Scholar. Submit the preprint to its index once the SSRN or arXiv version is live.
- GitHub repo traffic insights. `Insights, Traffic` shows clones, views, and referring sources.
- Zenodo statistics on the DOI page show downloads and views.

## 6. After v1.0

The CHANGELOG anticipates ongoing updates. A sensible cadence:

- Monthly mapping refresh. MITRE ATLAS releases monthly. Sync the mapping file.
- Quarterly sub-technique review. Add new sub-techniques as adversary tradecraft evolves.
- Annual major review. Possible v2.0 if the structure needs revision.

Each tagged release picks up a new Zenodo DOI version. That produces a clean citation history.
