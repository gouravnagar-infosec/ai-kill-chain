# Worked case studies

Four scenarios walked through the kill chain end to end. Each is annotated with EKC sub-technique IDs and the detection signals that would have caught the activity earliest.

These case studies aggregate public reporting and use representative details rather than attempting forensic reconstruction of any single incident.

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
