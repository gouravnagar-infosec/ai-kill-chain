# EKC and OWASP Top 10 for Agentic Applications (2026) mapping

Cross-references between the OWASP Top 10 for Agentic Applications (2026 edition) and Extended Cyber Kill Chain stages and sub-techniques. New in EKC v1.1.

Source: OWASP GenAI Security Project, *OWASP Top 10 for Agentic Applications for 2026*, published December 9, 2025. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ . The OWASP document is licensed CC BY-SA 4.0. This file reproduces only the ten IDs and titles; the one-line summaries below are paraphrased.

## Relationship

The Agentic Top 10 is a risk list for teams building and running autonomous agents. It sits next to the LLM Top 10 (2025) rather than replacing it, and its Appendix A cross-references every ASI entry to LLM Top 10 categories. The EKC uses both. The LLM Top 10 covers the model-and-application surface. The Agentic Top 10 covers what changes once the model plans, calls tools, holds credentials, keeps memory, and talks to other agents.

Like the LLM list, the Agentic list says *what* can go wrong but not *when* in an intrusion it happens. The tables below give that view: each ASI entry mapped to the kill chain stages where it is exploited, and to the EKC sub-techniques that describe the adversary behavior.

## Mapping table

| OWASP ID | Risk (OWASP title) | What it covers (paraphrased) | Primary EKC stages | Notes |
|---|---|---|---|---|
| ASI01 | Agent Goal Hijack | An attacker redirects the agent's objective or plan through content the agent treats as instructions. | Stages 3, 4 (also 6) | The agentic successor to indirect prompt injection. Delivery is Stage 3 (web, email, documents, tool descriptions, crafted assistant links, on-screen content). The hijack itself is Stage 4. When tool output keeps re-steering the agent across turns, it is Stage 6 C2 (EKC-6.4, EKC-6.6). |
| ASI02 | Tool Misuse and Exploitation | The agent uses tools it is legitimately allowed to use in unsafe ways: destructive calls, cost blow-ups, data leakage. | Stage 4, Stage 7c (also 7a) | Stage 4 is the first unsafe invocation (EKC-4.3, EKC-4.6). The harm lands in Stage 7c (EKC-7c.1, EKC-7c.2, EKC-7c.5) or as exfiltration in Stage 7a. |
| ASI03 | Identity and Privilege Abuse | Agents inherit, cache, or pass along credentials and delegated rights that an attacker can ride or steal. | Stage 7c | EKC-7c.3 covers the agent acting with someone else's privileges. EKC-7c.6 (new in v1.1) covers the credentials leaving the agent: OAuth tokens, API keys, CI secrets. Confused-deputy invocation in Stage 4 (EKC-4.3) is the usual entry point. |
| ASI04 | Agentic Supply Chain Vulnerabilities | Tampered or malicious third-party tools, MCP servers, models, prompts, or agent registries enter the agent's runtime. | Stage 0, Stages 2, 3, 5 | Staged in the supply chain (EKC-0.2 to EKC-0.5), built in Stage 2 (EKC-2.3), delivered at MCP handshake (EKC-3.5) or as a peer agent (EKC-3.8), and persisted by installation (EKC-5.3, EKC-5.5). Rug pulls (AML.T0109) live here too. |
| ASI05 | Unexpected Code Execution (RCE) | Text or tool access turns into code execution: shell commands, sandbox escape, unsafe eval. | Stage 4 (also 2) | EKC-4.6 covers computer-use agents running commands on the host. AI-generated malware (EKC-2.5) is the weaponization-side counterpart. Classical post-exploitation after RCE follows the canonical kill chain. |
| ASI06 | Memory & Context Poisoning | Stored memory, RAG stores, summaries or embeddings are corrupted so later reasoning is biased or unsafe. | Stages 3, 4, 5, 6 | Single-session pollution is Stage 4 (EKC-4.5). Cross-session persistence is Stage 5 (EKC-5.1 per user, EKC-5.4 RAG, EKC-5.6 shared memory). Memory and RAG as a dead-drop are Stage 6 (EKC-6.2, EKC-6.3). Crafted assistant links (EKC-3.7) are a delivery path observed in the wild in 2026. |
| ASI07 | Insecure Inter-Agent Communication | Messages between agents lack authentication, integrity, or validation, so they can be spoofed, replayed, or injected into. | Stages 1, 3, 6, 7c | Peer discovery is Stage 1 (EKC-1.6). An impersonated or malicious peer is Stage 3 delivery (EKC-3.8). Mid-session instruction smuggling is Stage 6 (EKC-6.6). Compromise spreading across an agent fabric is Stage 7c (EKC-7c.4). |
| ASI08 | Cascading Failures | One fault or compromise spreads through connected agents, tools, and workflows. | Stage 7c (also 5) | A consequence rather than an entry point. In kill-chain terms it is the blast radius of EKC-7c.4 (recursive agent abuse) and EKC-5.6 (shared memory poisoning). The control question is how far one compromised agent can reach. |
| ASI09 | Human-Agent Trust Exploitation | People over-trust an agent's fluency or authority and approve harmful actions without checking. | Stage 3, Stage 7c | Not a single sub-technique. It shows up where a human sits in the loop: approving a tool call in Stage 7c, or clicking a "Summarize with AI" link in Stage 3 (EKC-3.7). It is the reason human-in-the-loop alone is not a sufficient Stage 7c control. |
| ASI10 | Rogue Agents | Compromised or misaligned agents drift from their intended behavior while looking normal. | Stages 5, 6, 7c | A modified agent definition (EKC-5.2) or contaminated workflow (EKC-5.5) gives the persistent rogue behavior. An agent used as a C2 implant is Stage 6 (EKC-6.1). Scheduled harmful actions are Stage 7c (EKC-7c.5). |

## Sub-technique cross-reference

The table below is generated from the `owasp_agentic` tags in [`data/ekc.yaml`](../data/ekc.yaml). Use it to go from an ASI entry straight to the EKC IDs to put in a detection rule or a threat report.

<!-- BEGIN GENERATED: agentic -->
<!-- Generated by tools/build.py from data/ekc.yaml. Edit the YAML, not this table. -->

| OWASP ID | Risk | EKC stages | EKC sub-techniques tagged with it |
|---|---|---|---|
| ASI01 | Agent Goal Hijack | 3, 4, 6 | EKC-3.1, EKC-3.3, EKC-3.4, EKC-3.5, EKC-3.6, EKC-3.7, EKC-3.9, EKC-4.1, EKC-4.2, EKC-6.4, EKC-6.6 |
| ASI02 | Tool Misuse and Exploitation | 4, 7a, 7c | EKC-4.3, EKC-4.6, EKC-7a, EKC-7c.1, EKC-7c.2, EKC-7c.5 |
| ASI03 | Identity and Privilege Abuse | 4, 7c | EKC-4.3, EKC-7c.2, EKC-7c.3, EKC-7c.6 |
| ASI04 | Agentic Supply Chain Vulnerabilities | 0, 2, 3, 5 | EKC-0.2, EKC-0.3, EKC-0.4, EKC-0.5, EKC-2.3, EKC-3.5, EKC-3.8, EKC-5.3, EKC-5.5 |
| ASI05 | Unexpected Code Execution (RCE) | 2, 4 | EKC-2.5, EKC-4.6 |
| ASI06 | Memory & Context Poisoning | 3, 4, 5, 6 | EKC-3.2, EKC-3.7, EKC-4.5, EKC-5.1, EKC-5.4, EKC-5.6, EKC-6.2, EKC-6.3, EKC-6.5 |
| ASI07 | Insecure Inter-Agent Communication | 1, 3, 6, 7c | EKC-1.6, EKC-3.8, EKC-6.6, EKC-7c.4 |
| ASI08 | Cascading Failures | 5, 7c | EKC-5.6, EKC-7c.4 |
| ASI09 | Human-Agent Trust Exploitation | 3 | EKC-3.7 |
| ASI10 | Rogue Agents | 5, 6, 7c | EKC-5.2, EKC-5.5, EKC-6.1, EKC-7c.5 |

<!-- END GENERATED: agentic -->

## Relationship to the LLM Top 10 mapping

OWASP's Appendix A ties each ASI entry back to LLM Top 10 (2025) categories. Read it next to [`owasp-llm-mapping.md`](./owasp-llm-mapping.md) and a split shows up. LLM01 (Prompt Injection) feeds ASI01, ASI03, ASI05, ASI06, ASI08 and ASI09. LLM06 (Excessive Agency) feeds ASI01, ASI02, ASI03, ASI07, ASI08 and ASI09. In kill-chain terms the LLM list is weighted toward Stages 3 and 4, where injection lands. The Agentic list is weighted toward Stages 5, 6 and 7c, where the agent holds state, keeps a channel open, and acts. A program that maps controls only to the LLM list will tend to stop at Stage 4.

## Reading the mapping

"We cover ASI06" is a question about which stages the controls reach. A memory-write review covers Stage 5. It does nothing for a crafted link that delivers the write (Stage 3) or for memory used as a dead-drop channel (Stage 6).

"We cover ASI07" is a question about identity and content. Signed Agent Cards (A2A v1.0) address impersonation at Stage 3. They do not stop a genuine but malicious peer from smuggling instructions mid-session at Stage 6. That needs context grounding and out-of-band approval.

"We cover ASI03" is a question about where the credential lives. Scoping the agent's own permissions limits Stage 7c.3. It does not stop the token from being lifted and replayed elsewhere (EKC-7c.6). That needs short-lived, audience-bound tokens and detection of token use from unexpected places.
