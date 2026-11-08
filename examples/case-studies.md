# Worked case studies

Eight scenarios walked through the kill chain end to end. Each is annotated with EKC sub-technique IDs and the detection signals that would have caught the activity earliest.

Cases 1 to 4 (v1.0) aggregate public reporting and use representative details rather than attempting forensic reconstruction of any single incident.

Cases 5 to 8 (added in v1.1) are named 2026 incidents and disclosures. Each one is reconstructed only from the public sources listed under it, and each is also catalogued as a MITRE ATLAS case study or vendor advisory so readers can compare the two mappings. Where a source does not say something, the walkthrough says so rather than filling the gap.

## Case 1. Indirect prompt injection of a browsing agent

**Scenario.** A user asks a browsing-capable AI agent to summarize an article on a third-party news site. The page contains attacker-controlled content invisible to the user (white text on white background, or hidden inside a structured-data block) telling the agent to read the user's other open tabs and post their contents to an attacker-controlled webhook.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No supply-chain step required. |
| 1 | EKC-1.3 (capability and tool enumeration) | The attacker previously confirmed that the targeted agent class supports both browsing and outbound HTTP requests. |
| 2 | EKC-2.1, EKC-2.2 | The attacker crafts a payload that exploits the agent's tendency to follow instructions in retrieved web content. |
| 3 | **EKC-3.1 (indirect prompt injection via web content)** | The user-initiated browse fetches the malicious page. |
| 4 | **EKC-4.2 (indirect injection success) and EKC-4.3 (confused-deputy tool invocation)** | The agent treats the hidden instructions as authoritative and invokes its HTTP tool with attacker-controlled arguments. |
| 5 | (none) | No persistence in this case. Single-session attack. |
| 6 | (none) | No C2 channel needed. |
| 7 | **EKC-7c.1 (tool-mediated lateral action) and EKC-7a (data exfiltration)** | The agent reads the user's other open-tab content and posts it to the webhook. |

**Earliest-detection signal.** Tool calls whose argument strings contain content traceable to a recently retrieved untrusted document. A defender with argument-lineage tracking on the browsing agent's HTTP tool would have caught the exfiltration call before it completed.

## Case 2. MCP server compromise via poisoned tool descriptions

**Scenario.** An organization installs a third-party MCP server published to a public registry to enable a workflow integration. The server's tool descriptions contain an instruction block that activates when a downstream agent queries on a specific keyword, redirecting the agent to use a different (attacker-controlled) tool variant that exfiltrates the query plus contextual data. This pattern is documented in MITRE ATLAS case studies including AML.CS0045 (Data Exfiltration via an MCP Server used by Cursor, January 2026) and AML.CS0049 (Supply Chain Compromise via Poisoned ClawdBot Skill, February 2026).

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | **EKC-0.5 (malicious MCP server / tool catalog entry)** | The compromise is staged into the public registry. No specific target has been engaged yet. |
| 1 | EKC-1.3 | Targets self-select by installing the connector. |
| 2 | EKC-2.3 (malicious tool / MCP package) | The payload is the tool description itself. |
| 3 | **EKC-3.5 (tool-description poisoning)** | The descriptions are delivered to the agent at MCP handshake. |
| 4 | EKC-4.3 (confused-deputy tool invocation) | The agent invokes the malicious tool variant when the trigger keyword appears. |
| 5 | **EKC-5.3 (malicious connector installation)** | Persistence is automatic once installed. The MCP server stays in place. |
| 6 | **EKC-6.4 (tool-output C2)** | The server can return new instructions in subsequent responses, steering further agent behavior. |
| 7 | EKC-7a and EKC-7c.1 | Sensitive context fields are exfiltrated. |

**Earliest-detection signal.** Static analysis of tool descriptions on first registration. Long instruction-like text inside a tool description is a strong indicator. Defender controls at Stage 0 (registry attestation, signed manifests) and Stage 5 (sandboxed MCP installation review) provide the earliest interruption points.

## Case 3. RAG corpus poisoning of an enterprise assistant

**Scenario.** A company runs an internal assistant that indexes support tickets, internal wikis, and documentation as a retrieval-augmented context source. An attacker (acting as an external customer) submits support tickets whose contents are designed to be ingested into the assistant's vector store. Some weeks later, an internal employee queries the assistant on a related topic, the poisoned context is retrieved, and the assistant follows the embedded instructions to disclose configuration data.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No model-supply-chain step. |
| 1 | EKC-1.5 (embedding / retrieval surface discovery) | The attacker confirms (through prior probing or public documentation) that submitted tickets reach the RAG corpus. |
| 2 | EKC-2.1 | The attacker crafts ticket text with latent instructions. |
| 3 | **EKC-3.2 (RAG corpus poisoning)** | The submission is the delivery vector. |
| 4 | EKC-4.2 (indirect injection success) | When an employee's query triggers retrieval, the assistant follows the embedded instructions. |
| 5 | **EKC-5.4 (RAG corpus persistence)** | The poisoned content survives re-indexing because nothing in the ingestion pipeline flags or removes instruction-like content. |
| 6 | **EKC-6.3 (RAG-mediated C2)** | The attacker can submit follow-up tickets to update the instructions, holding a C2 channel through the public support-ticket interface. |
| 7 | EKC-7a and EKC-7c.1 | Configuration data is disclosed through the assistant's normal response channel. Depending on the assistant's tool access, additional pivot actions are possible. |

**Earliest-detection signal.** Indirect-injection scanning on ingest. Instruction-like text inside a customer support ticket, or anomalously long structured directives, should flag the content for review before it reaches the vector store. Defender controls at Stage 3 (ingest-time filtering) and Stage 5 (corpus integrity audit) are the earliest interruption points.

## Case 4. API-based model extraction against a proprietary domain model

**Scenario.** A competitor obtains authenticated API access to a company's proprietary domain-specific model (a fine-tuned model trained on legal, medical, or financial corpora). Over a period of weeks, the competitor issues a high volume of carefully constructed queries designed to recover the model's decision boundary. A surrogate model is trained on the input-output pairs and replicates much of the original model's capability.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No supply-chain step. |
| 1 | EKC-1.1 (model fingerprinting), EKC-1.4 (guardrail mapping) | The attacker probes for the base model identity and the policy boundary. |
| 2 | (none) | No weapon construction. The attack is the query distribution itself. |
| 3 | (none) | The "delivery" is API query traffic, not anomalous from a network perspective. |
| 4 | (none) | No prompt-injection step. The model operates as designed. |
| 5 | (none) | No persistence required. |
| 6 | (none) | No C2 channel. The attack is one-directional query-response. |
| 7 | **EKC-7b.1 (API-based model extraction)** | The competitor reconstructs an approximation of the model. **EKC-7b.5 (capability mining)** also applies if the access is then resold or operationalized. |

**Earliest-detection signal.** Query-pattern analytics. Programmatic, low-template-entropy / high-input-entropy query patterns from a single authenticated identity over a sustained period are diagnostic of extraction even when individual queries are policy-compliant. Defender controls at Stage 7b (query-distribution monitoring, output watermarking, per-account query budgets) are the only effective interruption point. Earlier stages are not engaged.

**Why this case matters for the framework.** Case 4 is the cleanest illustration of why Stage 7b is a peer sub-stage rather than a variant of classical exfiltration. The whole attack lives in Stage 7. Classical DLP controls do not detect it. Stage 7b is structurally distinct and needs its own control set.

## Case 5. AI Recommendation Poisoning through crafted assistant links (2026)

**Scenario.** In February 2026 the Microsoft Defender Security Research Team reported websites and emails that use "Summarize with AI" buttons and share links to plant instructions in users' AI assistants. The link opens the assistant with a prompt already filled in through a URL parameter such as `?q=` or `?prompt=`. Besides asking for a summary, the prompt tells the assistant to remember the company as a trusted or authoritative source for future answers. Over 60 days of email traffic Microsoft found 50 distinct prompts from 31 companies across more than a dozen industries, including finance, health and legal services. Ready-made tooling (the CiteMET npm package and a web-based share-URL generator) makes the technique a copy-and-paste job. The actors were legitimate businesses chasing visibility, not criminals, which is part of what makes the case useful: the same delivery path works for anyone.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No supply-chain step. |
| 1 | EKC-1.3 (capability and tool enumeration) | The technique depends on public knowledge that the major assistants accept a prompt in the URL and keep long-term memory. |
| 2 | EKC-2.1 (adversarial prompt crafting) | The prompt pairs a harmless request ("summarize this page") with a memory instruction. Public tools generate the links. |
| 3 | **EKC-3.7 (crafted assistant link delivery)** | Delivered as a button on the company's own site, or as a link in email. |
| 4 | EKC-4.1 (direct prompt injection success), EKC-4.5 (memory or context pollution) | The attacker's text arrives in the user's own prompt box, so the assistant treats it as the user's request. Microsoft notes effectiveness varies by platform and over time. |
| 5 | **EKC-5.1 (persistent memory implant)** | Where the memory write lands, the "trusted source" preference persists across later, unrelated conversations. |
| 6 | (none) | No channel. The implant works on its own. |
| 7 | EKC-7a (impact variant) | The objective is biased recommendations: integrity harm to the user rather than data theft. ATLAS models this as AI Agent Response Biasing (AML.T0130). |

**Earliest-detection signal.** The link itself, before anyone clicks. Prefilled-prompt URLs pointing at assistant domains, carrying words like "remember", "trusted source" or "future conversations", are rare in normal traffic and easy to hunt in mail and proxy logs. Microsoft published Advanced Hunting queries for exactly this. [`detections/sigma/ekc_3.7_assistant_link_prefilled_memory_prompt.yml`](../detections/sigma/ekc_3.7_assistant_link_prefilled_memory_prompt.yml) is the proxy-log version. The second interruption point is Stage 5: users who can see and delete what their assistant remembered can undo the implant.

**Why the stage split matters here.** The kill chain separates the delivery (a link, Stage 3) from the persistence (a memory write, Stage 5). A team that only reviews memory contents will catch implants after the fact. A team that hunts links stops them on the way in.

**Sources.** Microsoft Security Blog, "Manipulating AI memory for profit: The rise of AI Recommendation Poisoning", February 10, 2026, https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/ . MITRE ATLAS case study AML.CS0072.

## Case 6. PleaseFix: zero-click hijack of an agentic browser (2026)

**Scenario.** On March 3, 2026 Zenity Labs disclosed PleaseFix, a family of vulnerabilities in agentic browsers, starting with Perplexity Comet. In the first exploit path, attacker-controlled content such as a calendar invite carries hidden instructions. Later, when the user asks the browser agent to handle an ordinary calendar task, the agent reads files from the local file system and sends them to an attacker endpoint, while still returning the answer the user expected. Zenity describes it as zero-click. In the second path, the attacker steers the agent's authorized password-manager workflow (Comet's 1Password integration) to pull individual credentials or take over the 1Password account. 1Password itself was not exploited; it confirmed the root cause sat in the browser's agent execution model. Perplexity fixed the browser-side issue before public disclosure. Zenity frames PleaseFix as ClickFix aimed at the agent instead of the human.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No supply-chain step. |
| 1 | EKC-1.3 (capability and tool enumeration) | The attack relies on the agent having file-system reach and a password-manager integration. |
| 2 | EKC-2.1 (adversarial prompt crafting) | Instructions are written to survive inside an ordinary-looking invite. |
| 3 | **EKC-3.3 (email or message-borne injection), EKC-3.9 (interface-layer injection against computer-use agents)** | The invite reaches the user's calendar unprompted. The agent encounters the payload as content it is reading on the user's behalf. |
| 4 | EKC-4.2 (indirect prompt injection success), **EKC-4.6 (computer-use action hijack)** | The agent follows the hidden instructions and performs local file reads and password-manager actions as if the user had asked. |
| 5 | (none) | Public material does not describe persistence. |
| 6 | (none) | Not described. |
| 7 | **EKC-7a (data exfiltration), EKC-7c.6 (agent credential and token theft)** | Local files leave the machine. Credentials leave the password manager through the agent's own granted access. |

**Earliest-detection signal.** The agent opening `file://` paths that the user's task never mentioned. That action has no innocent reason in a calendar task, and it happens before anything leaves the machine. [`detections/sigma/ekc_4.6_computer_use_agent_local_navigation.yml`](../detections/sigma/ekc_4.6_computer_use_agent_local_navigation.yml) covers it. The structural fix is Stage 4: a computer-use agent should not run with the user's real file system and vault in reach.

**Why EKC-7c.6 matters here.** Once a credential is pulled out through the agent, the attacker no longer needs the agent, the browser, or the injection. Controls that only watch agent behavior (Stage 4) miss what happens next with the stolen credential.

**Sources.** Zenity Labs, "Zenity Labs Discloses PleaseFix Vulnerability Family in Perplexity Comet and Other Agentic Browsers", March 3, 2026, https://zenity.io/company-overview/newsroom/company-news/zenity-labs-discloses-pleasefix-perplexedagent-vulnerability . Related ATLAS material: AI ClickFix (AML.CS0055) and Machine Compromise: Local AI Agent (AML.T0112.000).

## Case 7. Secret exposure through an AI coding agent in CI/CD (2026)

**Scenario.** On June 5, 2026 Microsoft Threat Intelligence (Dor Edry and Amit Eliahu) published how the Claude Code GitHub Action could leak workflow secrets. The action runs an agent over GitHub content, including issue bodies, pull request descriptions and comments that anyone may be able to write. Claude Code scrubbed environment variables for subprocesses such as Bash, but the Read tool did not have the same restriction. Steered by untrusted issue content, the agent could read `/proc/self/environ` and expose `ANTHROPIC_API_KEY` along with other credentials on the runner. To get past GitHub's secret scanning, the researchers had the model drop the first seven characters of the key before printing it; the attacker adds `sk-ant-` back afterwards. Exfiltration routes depended on the workflow, for example an issue comment, or the action log when full output is enabled. Microsoft reported the issue through HackerOne on April 29, 2026. Anthropic blocked access to sensitive `/proc` files in Claude Code 2.1.128 on May 5, 2026.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No supply-chain step. |
| 1 | EKC-1.3 (capability and tool enumeration) | Workflow files in public repositories show which tools the agent has and which events trigger it. ATLAS records this as Discover AI Agent Configuration: Tool Definitions and Activation Triggers. |
| 2 | EKC-2.1, EKC-2.4 (jailbreak chain assembly) | The payload is written to look like a reasonable request inside an issue. |
| 3 | **EKC-3.3 (email or message-borne injection)** | Issues, PR descriptions and comments are messages the agent is configured to read. |
| 4 | EKC-4.2 (indirect injection success), **EKC-4.3 (confused-deputy tool invocation)**, EKC-4.4 (guardrail or classifier bypass) | The agent uses its own Read tool on the process environment. Altering the key defeats secret scanning. |
| 5 | (none) | Not required. |
| 6 | (none) | Not required. |
| 7 | **EKC-7c.6 (agent credential and token theft)**, EKC-7a | The API key leaves through a channel the workflow already allows. |

**Earliest-detection signal.** An agent read of `/proc/self/environ` or similar credential paths. Coding agents do not need their own environment to triage an issue. [`detections/sigma/ekc_7c.6_agent_reads_credentials.yml`](../detections/sigma/ekc_7c.6_agent_reads_credentials.yml) covers it. Microsoft's recommended architecture control is Meta's "Agents Rule of Two": do not let one workflow process untrusted input, hold secrets, and change state or talk externally all at once.

**Why the per-tool fix is not enough.** The Stage 4 fix (block `/proc` reads) closes this path. The Stage 7c.6 control (scoped, short-lived keys, one per workflow, with usage monitoring) limits the damage from the next path nobody has found yet.

**Sources.** Microsoft Security Blog, "Securing CI/CD in an agentic world: Claude Code GitHub action case", June 5, 2026, https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/ . MITRE ATLAS case study AML.CS0067.

## Case 8. A multi-agent framework runs an intrusion against government systems (2026)

**Scenario.** Between July 1 and July 4, 2026 an attacker used a framework of AI agents, built on the open-source Hermes Agent and OpenClaw projects, against Taiwanese government systems. Dream Research Labs published an analysis on August 12, 2026 after finding the attacker's workspace. Up to eight lettered sub-agents ran in parallel per wave, across twelve waves. A planning loop scored fourteen candidate attack chains and fed each wave's after-action reports into the next. Initial access came from ordinary weaknesses found at machine speed: three hidden debug API endpoints that returned an authenticated session for any request, an unauthenticated users API, a JWT check that accepted `alg: none`, and password spraying against an office portal with Tesseract OCR solving the CAPTCHA. Eighty-five accounts fell. Eighty-four of them reached an internal system because its SSO bridge trusted the portal session with no MFA. The operation took more than 2,564 personnel records, seven SSO client secrets and six database credentials. An uploaded web shell was blocked from executing. Taiwan's Ministry of Digital Affairs confirmed an AI-assisted attack and described it as a hybrid of human operators and agents. Dream's linguistic analysis points to a Chinese-language operator; no government has publicly attributed it.

This case is different from the other seven. The victim did not run an AI system that was attacked. The adversary ran one.

**Kill chain walkthrough.**

| Stage | Sub-technique | What happened |
|---|---|---|
| 0 | (none) | No AI supply chain involved on the victim side. |
| 1 | Classical reconnaissance, run by agents | Sub-agents mapped exposed endpoints and harvested employee identifiers. ATLAS: Autonomous Reconnaissance (AML.T0116). |
| 2 | EKC-2.5 (AI-generated polymorphic malware), loosely | Tooling and payloads were produced and revised by the agents between waves. The reporting does not describe malware variants specifically. |
| 3 | Classical delivery | Requests to exposed APIs and a login portal. |
| 4 | Classical exploitation | Debug endpoints, JWT `alg: none`, credential spraying with OCR. |
| 5 | Classical installation | Dream reports a persistent foothold; the web shell did not execute. |
| 6 | Classical C2 | Not detailed in the reporting. |
| 7 | **EKC-7a (data exfiltration)** | Personnel records, client secrets and database credentials. |

**Earliest-detection signal.** Volume and tempo. Spraying across a portal with near-perfect CAPTCHA solving, and repeated calls to undocumented debug endpoints, both stand out against human traffic. The SSO bridge was the single control that turned 85 portal accounts into internal access.

**Where the EKC helps, and where it stops.** The canonical stages still describe this intrusion. It moved through reconnaissance, access, persistence and exfiltration like any other, and ordinary Stage 4 and Stage 5 controls (MFA on the SSO bridge, no debug endpoints in production) would have broken it. What changes is speed and parallelism. Twelve waves in four days, with the plan updated between waves, compresses the time a SOC has between Stage 1 and Stage 7. The EKC does not yet have sub-techniques for adversary-operated agent swarms, because v1.x describes attacks *on* and *through* the defender's AI systems. ATLAS now catalogs the attacker side (Autonomous Attack Orchestration AML.T0124, Autonomous Attack-Path Adaptation AML.T0117). A future EKC release may add a cross-cutting note for it; it would not be a new stage.

**Sources.** Dream Research Labs, "Inside a Multi-Agent AI Framework Used to Compromise Government Entities in Asia", August 12, 2026, https://dreamgroup.com/blog/inside-a-multi-agent-ai-framework-used-to-compromise-government-entities-in-asia . Taiwan Ministry of Digital Affairs press release, https://moda.gov.tw/ACS/press/news/press/20394 . MITRE ATLAS case study AML.CS0071. AI Incident Database incident 1646.
