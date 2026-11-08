# EKC and MITRE ATLAS mapping

Cross-references between Extended Cyber Kill Chain sub-techniques and MITRE ATLAS tactics, techniques, and case studies. ATLAS reference version: **v2026.10**, released October 28, 2026 (data format 6.1.0).

## Relationship

ATLAS is an adversary model for AI systems organized as a 16-tactic matrix. As of v2026.10 it holds 129 techniques, 92 sub-techniques, 44 mitigations, and 77 case studies. The EKC absorbs AI-era threats into the seven-stage Lockheed Martin temporal structure plus a new Stage 0. The two frameworks are complementary. This mapping is one-to-many in both directions because one ATLAS technique can surface at multiple kill chain stages, and one EKC sub-technique can compose multiple ATLAS techniques.

## How this file is produced

The two tables below are generated. The cross-references live in [`data/ekc.yaml`](../data/ekc.yaml). `tools/build.py` resolves every ATLAS ID against a vendored index of the official release ([`data/vendor/atlas-index.json`](../data/vendor/atlas-index.json), built from `mitre-atlas/atlas-data`), fills in the current ATLAS name and tactic, and writes the tables. If an ID does not exist in the pinned release, or a technique was moved, the build fails. That is how the v1.1 refresh caught the corrections listed further down.

To move to a newer ATLAS release: clone `mitre-atlas/atlas-data`, run `python tools/refresh_atlas.py <path>/dist/v6/ATLAS-<version>.yaml`, bump `reference_versions.mitre_atlas` in `data/ekc.yaml`, and run `python tools/build.py`. Every broken reference is listed in one pass.

## ATLAS changes since v5.4.0 that affect this mapping

v1.0 tracked ATLAS v5.4.0 (February 2026). Between then and v2026.10 MITRE made several changes that touch EKC cross-references:

- **New version scheme.** From May 2026 (v2026.05), ATLAS content releases are numbered YYYY.MM and the data format is versioned separately (6.0.0, then 6.1.0). v5.4.0 corresponds to content release 2026.02.
- **Tool poisoning moved.** Publish Poisoned AI Agent Tool (AML.T0104, added in v5.4.0) became Publish Poisoned AI Artifacts: AI Agent Tools (AML.T0115.002) in v2026.07. The same release added AI Agent Tool Poisoning sub-techniques for Definition and Instructions (AML.T0110.000), Implementation (AML.T0110.001), and Runtime Response (AML.T0110.002).
- **Inference-API exfiltration split up.** In v2026.10, Infer Training Data Membership moved from AML.T0024.000 to Training Data Information from AI Models: Infer Membership (AML.T0137.000). Extract Memorized Data (AML.T0137.003) and Outputs from AI Models (AML.T0135) were added. Extract LLM System Prompt (AML.T0056) became Data from AI Services: System Instructions (AML.T0085.003).
- **Renames.** AML.T0020 Poison Training Data became Training Data Poisoning (v2026.07). AML.T0010 AI Supply Chain Compromise became Supply Chain Compromise, with sub-techniques Software, Data Repository, and Model Repository (v2026.10). AML.T0005 Create Proxy AI Model became Replicate AI Model Behavior (v2026.10). AML.T0075 Cloud Service Discovery became Enterprise Resource Discovery (v2026.08). The AI Attack Staging tactic (AML.TA0001) became AI Attack Adaptation (v2026.08).
- **New agentic coverage used by v1.1.** Crafted AI Assistant Links (AML.T0131), Discover AI Agent Runtime Capabilities (AML.T0133), AI Targeted Cloaking (AML.T0134), and Triggers in Multimodal Inputs (AML.T0129) in v2026.09. LLM Prompt Propagation (AML.T0143) in v2026.10. Autonomous AI Agent Communication (AML.T0118) in v2026.08. Machine Compromise: Local AI Agent (AML.T0112.000) and AI Supply Chain Rug Pull (AML.T0109) in v5.5.0.

## Corrections to v1.0 cross-references

Re-validating against MITRE's data also surfaced errors that were already present in v1.0. They are fixed in v1.1:

- EKC-4.5, EKC-5.1 and EKC-6.2 cited AML.T0080.001 as "AI Agent Context Poisoning: Memory". Memory is AML.T0080.000. AML.T0080.001 is Thread. EKC-4.5 (single-session pollution) now cites Thread first; EKC-5.1 and EKC-6.2 cite Memory.
- EKC-7b.5 cited the LLMjacking case study as AML.CS0029. AML.CS0029 is Google Bard Conversation Exfiltration. LLMjacking is AML.CS0030.
- EKC-3.2 cited RAG Credential Harvesting (AML.T0082), which is a Credential Access technique. RAG corpus poisoning now maps to RAG Poisoning (AML.T0070) and Retrieval Content Crafting (AML.T0066).
- EKC-7c.4 cited AI Agent (AML.T0108). In ATLAS that technique sits under Command and Control: abusing an agent on the victim's system as a C2 implant. It now maps to EKC-6.1 and EKC-6.4. EKC-7c.4 maps to LLM Prompt Propagation (AML.T0143) instead.
- The v1.0 reverse view used the tactic labels "ML Model Access" and "ML Attack Staging". ATLAS v5.4.0 already called them AI Model Access and AI Attack Staging.
- Several v1.0 rows named techniques without IDs (Extract ML Model, Create Proxy ML Model, Craft Adversarial Data, Extract Training Data). Every row now carries resolved IDs.

## Mapping table

<!-- BEGIN GENERATED: forward -->
<!-- Generated by tools/build.py from data/ekc.yaml. Edit the YAML, not this table. -->

| EKC ID | Sub-technique | ATLAS tactics | ATLAS techniques | ATLAS case studies |
|---|---|---|---|---|
| EKC-0.1 | Training data poisoning | Resource Development; Initial Access; Persistence | Training Data Poisoning (AML.T0020); Supply Chain Compromise: Data Repository (AML.T0010.002); Publish Poisoned AI Artifacts: Datasets (AML.T0115.000) |  |
| EKC-0.2 | Fine-tuning backdoor | Resource Development; Persistence; AI Attack Adaptation | Manipulate AI Model: Poison AI Model (AML.T0018.000); Craft Adversarial Data: Insert Backdoor Trigger (AML.T0043.004); Publish Poisoned AI Artifacts: Models (AML.T0115.001) |  |
| EKC-0.3 | Pre-trained model trojan | Resource Development; Initial Access; Defense Evasion | Supply Chain Compromise: Model Repository (AML.T0010.003); Publish Poisoned AI Artifacts: Models (AML.T0115.001); AI Supply Chain Reputation Inflation (AML.T0111) | AML.CS0019; AML.CS0065 |
| EKC-0.4 | Tokenizer or preprocessing manipulation | Initial Access; Persistence; AI Attack Adaptation | Supply Chain Compromise: Software (AML.T0010.001); Manipulate AI Model: Modify Prompt Construction Logic (AML.T0018.003) | AML.CS0064 |
| EKC-0.5 | Malicious MCP server or tool catalog entry | Resource Development; Initial Access; Persistence; Defense Evasion | Publish Poisoned AI Artifacts: AI Agent Tools (AML.T0115.002); AI Agent Tool Poisoning: Definition and Instructions (AML.T0110.000); Supply Chain Compromise: AI Agent Tool (AML.T0010.005); AI Supply Chain Rug Pull (AML.T0109) | AML.CS0049; AML.CS0053 |
| EKC-1.1 | Model fingerprinting | Reconnaissance; Discovery | Discover AI Model Family (AML.T0014); Active Scanning (AML.T0006); Discover AI Model Outputs (AML.T0063) |  |
| EKC-1.2 | System prompt enumeration | Discovery | Discover LLM System Information: System Prompt (AML.T0069.002); Discover AI Agent Configuration: Embedded Knowledge (AML.T0084.000) |  |
| EKC-1.3 | Capability and tool enumeration | Discovery | Discover AI Agent Configuration: Tool Definitions (AML.T0084.001); Discover AI Agent Runtime Capabilities (AML.T0133); Enterprise Resource Discovery (AML.T0075) |  |
| EKC-1.4 | Guardrail mapping | Reconnaissance; Discovery | Discover LLM System Information (AML.T0069); Active Scanning: Probe AI Agent Trigger Channels (AML.T0006.003); Search Open Websites/Domains (AML.T0095) |  |
| EKC-1.5 | Embedding and retrieval surface discovery | Reconnaissance; Discovery; Collection | Gather RAG-Indexed Targets (AML.T0064); Discover AI Agent Configuration (AML.T0084); Data from AI Services: RAG Databases (AML.T0085.000) |  |
| EKC-1.6 | Peer agent and Agent Card enumeration (new in 1.1) | Resource Development; Discovery | Discover AI Agent Runtime Capabilities (AML.T0133); Discover AI Agent Configuration: Call Chains (AML.T0084.003); Acquire Public AI Artifacts: AI Agent Configuration (AML.T0002.002) |  |
| EKC-2.1 | Adversarial prompt crafting | Defense Evasion; AI Attack Adaptation | LLM Prompt Crafting (AML.T0065); LLM Prompt Obfuscation (AML.T0068) |  |
| EKC-2.2 | Multi-modal payload construction | Defense Evasion; AI Attack Adaptation | LLM Prompt Crafting (AML.T0065); Triggers in Multimodal Inputs (AML.T0129) |  |
| EKC-2.3 | Malicious tool or MCP package | Resource Development | Develop Capabilities: AI Agent Tools (AML.T0017.002); Publish Poisoned AI Artifacts: AI Agent Tools (AML.T0115.002) |  |
| EKC-2.4 | Jailbreak chain assembly | Privilege Escalation; Defense Evasion; AI Attack Adaptation | LLM Jailbreak (AML.T0054); LLM Prompt Crafting (AML.T0065); LLM Prompt Obfuscation (AML.T0068) |  |
| EKC-2.5 | AI-generated polymorphic malware | Resource Development; AI Attack Adaptation | Obtain Capabilities: Generative AI (AML.T0016.002); Develop Capabilities: Malware (AML.T0017.003); Generate Malicious Commands (AML.T0102) | AML.CS0044 |
| EKC-3.1 | Indirect prompt injection via web content | Initial Access; Execution; Defense Evasion | LLM Prompt Injection: Indirect (AML.T0051.001); Drive-by Compromise (AML.T0078); AI Targeted Cloaking (AML.T0134) |  |
| EKC-3.2 | RAG corpus poisoning | Persistence; AI Attack Adaptation | RAG Poisoning (AML.T0070); Retrieval Content Crafting (AML.T0066); AI Agent Tool Data Poisoning (AML.T0099) |  |
| EKC-3.3 | Email or message-borne injection | Initial Access; Execution; Persistence | LLM Prompt Injection: Indirect (AML.T0051.001); Prompt Infiltration via Public-Facing Application (AML.T0093) | AML.CS0059; AML.CS0063 |
| EKC-3.4 | Document-borne injection | Initial Access; Execution; Persistence | LLM Prompt Injection: Indirect (AML.T0051.001); Prompt Infiltration via Public-Facing Application (AML.T0093) |  |
| EKC-3.5 | Tool-description poisoning | Execution; Persistence | AI Agent Tool Poisoning: Definition and Instructions (AML.T0110.000); User Execution: Poisoned AI Agent Tool (AML.T0011.002) |  |
| EKC-3.6 | Image, audio, or QR-code injection | Execution; Defense Evasion | LLM Prompt Injection: Indirect (AML.T0051.001); Triggers in Multimodal Inputs (AML.T0129) |  |
| EKC-3.7 | Crafted assistant link delivery (new in 1.1) | Initial Access; Defense Evasion | Crafted AI Assistant Links (AML.T0131); LLM Prompt Obfuscation (AML.T0068) | AML.CS0072 |
| EKC-3.8 | Malicious or impersonated peer agent (new in 1.1) | Execution; Defense Evasion | Impersonation (AML.T0073); LLM Prompt Injection: Indirect (AML.T0051.001) |  |
| EKC-3.9 | Interface-layer injection against computer-use agents (new in 1.1) | Execution; Defense Evasion | AI Agent Clickbait (AML.T0100); AI Targeted Cloaking (AML.T0134); Triggers in Multimodal Inputs (AML.T0129) | AML.CS0055 |
| EKC-4.1 | Direct prompt injection success | Execution | LLM Prompt Injection: Direct (AML.T0051.000) |  |
| EKC-4.2 | Indirect prompt injection success | Execution | LLM Prompt Injection: Indirect (AML.T0051.001); LLM Prompt Injection: Triggered (AML.T0051.002) |  |
| EKC-4.3 | Confused-deputy tool invocation | Execution; Privilege Escalation; Lateral Movement | AI Agent Tool Invocation (AML.T0053); AI Agent Clickbait (AML.T0100) |  |
| EKC-4.4 | Guardrail or classifier bypass | Initial Access; Privilege Escalation; Defense Evasion; Impact | LLM Jailbreak (AML.T0054); Evade AI Model (AML.T0015); LLM Prompt Obfuscation (AML.T0068) |  |
| EKC-4.5 | Memory or context pollution | Persistence; Defense Evasion | AI Agent Context Poisoning: Thread (AML.T0080.001); AI Agent Context Poisoning: Memory (AML.T0080.000); Manipulate User LLM Chat History (AML.T0092) |  |
| EKC-4.6 | Computer-use action hijack (new in 1.1) | Execution; Privilege Escalation; Lateral Movement; Impact | Machine Compromise: Local AI Agent (AML.T0112.000); AI Agent Tool Invocation (AML.T0053); Data Destruction via AI Agent Tool Invocation (AML.T0101) | AML.CS0046; AML.CS0055 |
| EKC-5.1 | Persistent memory implant | Persistence | AI Agent Context Poisoning: Memory (AML.T0080.000) | AML.CS0040; AML.CS0066 |
| EKC-5.2 | System prompt override | Persistence; Defense Evasion; AI Attack Adaptation | Modify AI Agent Configuration (AML.T0081); Manipulate AI Model: Modify Prompt Construction Logic (AML.T0018.003) |  |
| EKC-5.3 | Malicious connector installation | Execution; Persistence; Defense Evasion | Modify AI Agent Configuration (AML.T0081); User Execution: Poisoned AI Agent Tool (AML.T0011.002); Deploy AI Agent (AML.T0103) |  |
| EKC-5.4 | RAG corpus persistence | Persistence; Defense Evasion | RAG Poisoning (AML.T0070); Delay Execution of LLM Instructions (AML.T0094) |  |
| EKC-5.5 | Stored skill or workflow contamination | Persistence; Defense Evasion | Modify AI Agent Configuration (AML.T0081); Event Triggered Execution (AML.T0142) | AML.CS0049 |
| EKC-5.6 | Shared agent memory poisoning (new in 1.1) | Persistence; Lateral Movement | AI Agent Context Poisoning: Memory (AML.T0080.000); LLM Prompt Propagation (AML.T0143); LLM Prompt Self-Replication (AML.T0061) |  |
| EKC-6.1 | LLM channel as C2 | Command and Control | AI Service API (AML.T0096); AI Service Web Interface (AML.T0114); AI Agent (AML.T0108) | AML.CS0042; AML.CS0051; AML.CS0061 |
| EKC-6.2 | Memory-mediated C2 | Persistence | AI Agent Context Poisoning: Memory (AML.T0080.000) |  |
| EKC-6.3 | RAG-mediated C2 | Persistence | RAG Poisoning (AML.T0070); AI Agent Tool Data Poisoning (AML.T0099) |  |
| EKC-6.4 | Tool-output C2 | Persistence; Command and Control | AI Agent Tool Poisoning: Runtime Response (AML.T0110.002); AI Agent (AML.T0108) |  |
| EKC-6.5 | Cross-session steganographic C2 | Defense Evasion | LLM Prompt Obfuscation (AML.T0068); Delay Execution of LLM Instructions (AML.T0094) | AML.CS0038 |
| EKC-6.6 | Inter-agent session smuggling (new in 1.1) | Execution; Persistence | LLM Prompt Injection: Indirect (AML.T0051.001); AI Agent Context Poisoning: Thread (AML.T0080.001) |  |
| EKC-7a | Classical data exfiltration | Collection; Exfiltration | Exfiltration via AI Inference API (AML.T0024); Exfiltration via AI Agent Tool Invocation (AML.T0086); Exfiltration via AI User Interface (AML.T0136); Data from AI Services (AML.T0085); Exfiltration via Cyber Means (AML.T0025) |  |
| EKC-7b.1 | API-based model extraction | Resource Development; Discovery; Collection; AI Attack Adaptation | Replicate AI Model Behavior (AML.T0005); Replicate AI Model Behavior: Replicate Behavior from Model Outputs (AML.T0005.001); Outputs from AI Models (AML.T0135); Recover AI Model Internals (AML.T0144) | AML.CS0056; AML.CS0058; AML.CS0075; AML.CS0076 |
| EKC-7b.2 | Training-data extraction | Collection | Training Data Information from AI Models: Extract Memorized Data (AML.T0137.003) |  |
| EKC-7b.3 | Membership inference | Collection | Training Data Information from AI Models: Infer Membership (AML.T0137.000) |  |
| EKC-7b.4 | System prompt and instruction extraction | Discovery; Collection | Data from AI Services: System Instructions (AML.T0085.003); Discover LLM System Information: System Prompt (AML.T0069.002) |  |
| EKC-7b.5 | Capability mining | AI Model Access; Impact | AI-Enabled Product or Service (AML.T0047); Cost Harvesting (AML.T0034) | AML.CS0030 |
| EKC-7c.1 | Tool-mediated lateral action | Execution; Privilege Escalation; Lateral Movement; Exfiltration | AI Agent Tool Invocation (AML.T0053); Exfiltration via AI Agent Tool Invocation (AML.T0086) |  |
| EKC-7c.2 | Cross-app pivot | Credential Access; Lateral Movement | Use Alternate Authentication Material (AML.T0091); AI Agent Tool Credential Harvesting (AML.T0098); LLM Prompt Propagation (AML.T0143) |  |
| EKC-7c.3 | Identity confusion attack | Lateral Movement | Use Alternate Authentication Material: Application Access Token (AML.T0091.000) |  |
| EKC-7c.4 | Recursive agent abuse | Execution; Lateral Movement | LLM Prompt Propagation (AML.T0143); Deploy AI Agent (AML.T0103) |  |
| EKC-7c.5 | Workflow weaponization | Persistence; Defense Evasion; Impact | Modify AI Agent Configuration (AML.T0081); Data Destruction via AI Agent Tool Invocation (AML.T0101); Event Triggered Execution (AML.T0142) |  |
| EKC-7c.6 | Agent credential and token theft (new in 1.1) | Credential Access; Lateral Movement | AI Agent Tool Credential Harvesting (AML.T0098); Credentials from AI Agent Configuration (AML.T0083); Unsecured Credentials (AML.T0055); Use Alternate Authentication Material: Application Access Token (AML.T0091.000); Steal Web Session Cookie (AML.T0113) | AML.CS0048; AML.CS0067 |

<!-- END GENERATED: forward -->

## Reverse view: ATLAS tactics surfacing at each EKC stage

The forward table above is EKC-first. This reverse view is ATLAS-first, for a defender or red teamer who arrives via the ATLAS matrix and needs to locate the equivalent kill chain stage. Rows follow the column order of the v2026.10 ATLAS matrix.

<!-- BEGIN GENERATED: reverse -->
<!-- Generated by tools/build.py from data/ekc.yaml. Edit the YAML, not this table. -->

| ATLAS tactic | EKC stages where it surfaces | EKC sub-techniques |
|---|---|---|
| Reconnaissance (AML.TA0002) | Stage 1 | EKC-1.1, EKC-1.4, EKC-1.5 |
| Resource Development (AML.TA0003) | Stage 0; Stage 1; Stage 2; Stage 7b | EKC-0.1, EKC-0.2, EKC-0.3, EKC-0.5, EKC-1.6, EKC-2.3, EKC-2.5, EKC-7b.1 |
| Initial Access (AML.TA0004) | Stage 0; Stage 3; Stage 4 | EKC-0.1, EKC-0.3, EKC-0.4, EKC-0.5, EKC-3.1, EKC-3.3, EKC-3.4, EKC-3.7, EKC-4.4 |
| AI Model Access (AML.TA0000) | Stage 7b | EKC-7b.5 |
| Execution (AML.TA0005) | Stage 3; Stage 4; Stage 5; Stage 6; Stage 7c | EKC-3.1, EKC-3.3, EKC-3.4, EKC-3.5, EKC-3.6, EKC-3.8, EKC-3.9, EKC-4.1, EKC-4.2, EKC-4.3, EKC-4.6, EKC-5.3, EKC-6.6, EKC-7c.1, EKC-7c.4 |
| Persistence (AML.TA0006) | Stage 0; Stage 3; Stage 4; Stage 5; Stage 6; Stage 7c | EKC-0.1, EKC-0.2, EKC-0.4, EKC-0.5, EKC-3.2, EKC-3.3, EKC-3.4, EKC-3.5, EKC-4.5, EKC-5.1, EKC-5.2, EKC-5.3, EKC-5.4, EKC-5.5, EKC-5.6, EKC-6.2, EKC-6.3, EKC-6.4, EKC-6.6, EKC-7c.5 |
| Privilege Escalation (AML.TA0012) | Stage 2; Stage 4; Stage 7c | EKC-2.4, EKC-4.3, EKC-4.4, EKC-4.6, EKC-7c.1 |
| Defense Evasion (AML.TA0007) | Stage 0; Stage 2; Stage 3; Stage 4; Stage 5; Stage 6; Stage 7c | EKC-0.3, EKC-0.5, EKC-2.1, EKC-2.2, EKC-2.4, EKC-3.1, EKC-3.6, EKC-3.7, EKC-3.8, EKC-3.9, EKC-4.4, EKC-4.5, EKC-5.2, EKC-5.3, EKC-5.4, EKC-5.5, EKC-6.5, EKC-7c.5 |
| Credential Access (AML.TA0013) | Stage 7c | EKC-7c.2, EKC-7c.6 |
| Discovery (AML.TA0008) | Stage 1; Stage 7b | EKC-1.1, EKC-1.2, EKC-1.3, EKC-1.4, EKC-1.5, EKC-1.6, EKC-7b.1, EKC-7b.4 |
| Lateral Movement (AML.TA0015) | Stage 4; Stage 5; Stage 7c | EKC-4.3, EKC-4.6, EKC-5.6, EKC-7c.1, EKC-7c.2, EKC-7c.3, EKC-7c.4, EKC-7c.6 |
| Collection (AML.TA0009) | Stage 1; Stage 7a; Stage 7b | EKC-1.5, EKC-7a, EKC-7b.1, EKC-7b.2, EKC-7b.3, EKC-7b.4 |
| AI Attack Adaptation (AML.TA0001) | Stage 0; Stage 2; Stage 3; Stage 5; Stage 7b | EKC-0.2, EKC-0.4, EKC-2.1, EKC-2.2, EKC-2.4, EKC-2.5, EKC-3.2, EKC-5.2, EKC-7b.1 |
| Command and Control (AML.TA0014) | Stage 6 | EKC-6.1, EKC-6.4 |
| Exfiltration (AML.TA0010) | Stage 7a; Stage 7c | EKC-7a, EKC-7c.1 |
| Impact (AML.TA0011) | Stage 4; Stage 7b; Stage 7c | EKC-4.4, EKC-4.6, EKC-7b.5, EKC-7c.5 |

<!-- END GENERATED: reverse -->

Four structural observations from the reverse view.

First, ATLAS Persistence collapses what the kill chain separates into Stage 4 (a single-session memory or thread pollution event) and Stage 5 (cross-session installation). The kill-chain split matters for defender control placement: Stage 4 controls run at the conversation surface; Stage 5 controls run on the memory and configuration stores.

Second, ATLAS Lateral Movement, Credential Access and Privilege Escalation all surface inside EKC Stage 7c. The kill chain treats agentic pivot as a single sub-stage of Actions on Objectives because the adversary's goal is mission completion. The tactic distinction matters less for SOC playbook design than for red-team taxonomy. EKC-7c.6 (agent credential and token theft) is where Credential Access lands now that agents broker OAuth tokens and API keys on the user's behalf.

Third, Stage 7b no longer surfaces under ATLAS Exfiltration. In v2026.10 MITRE moved membership inference, memorized-data extraction and output harvesting into Collection (AML.T0137, AML.T0135), and model replication sits under Resource Development and AI Attack Adaptation (AML.T0005). ATLAS now treats "gathering the model's knowledge" as collection and "building a copy" as preparation. The EKC keeps all of it in Stage 7b because, for the defender, the control set is the same: query-pattern analytics, per-account query budgets and output watermarking on the inference surface.

Fourth, ATLAS has no technique yet for a malicious or impersonated *peer* agent in a delegation protocol such as A2A (EKC-3.8). AML.T0118 Autonomous AI Agent Communication describes adversary-operated agents talking to each other, which is the attacker's own tooling rather than an attack on the victim's agent fabric. EKC-3.8 cites the nearest techniques (Impersonation, indirect prompt injection) and should be re-mapped when ATLAS adds coverage.

## Notes on the mapping

The EKC puts agentic pivot, credential theft and memory-mediated C2 inside Stage 7c and Stage 6 (kill chain stages). ATLAS catalogs the same primitive techniques under its tactics matrix (Lateral Movement AML.TA0015, Credential Access AML.TA0013, Command and Control AML.TA0014). Defenders who reason in kill-chain stages get the temporal view from the EKC. Defenders who reason in tactics matrices get the catalog view from ATLAS.

ATLAS IDs, names, and tactic assignments above come from the official `mitre-atlas/atlas-data` release `dist/v6/ATLAS-2026.10.yaml`. ATLAS keeps a monthly release cadence, so names will keep evolving. The build pins one release at a time so this file never mixes versions.

For authoritative definitions, see https://atlas.mitre.org and https://github.com/mitre-atlas/atlas-data.
