# EKC and MITRE ATLAS mapping

Cross-references between Extended Cyber Kill Chain sub-techniques and MITRE ATLAS tactics and techniques. ATLAS reference version: v5.4.0, released February 2026.

## Relationship

ATLAS is an adversary model for AI systems organized as a 16-tactic matrix (84 techniques, 56 sub-techniques, 32 mitigations, 42 case studies as of v5.4.0). The EKC absorbs AI-era threats into the seven-stage Lockheed Martin temporal structure plus a new Stage 0. The two frameworks are complementary. This mapping is one-to-many in both directions because one ATLAS technique can surface at multiple kill chain stages, and one EKC sub-technique can compose multiple ATLAS techniques.

Recent ATLAS evolution worth noting:

- v4.9.0 (April 2025) added Command and Control as a tactic (AML.TA0014).
- v5.1.0 (November 2025) added Lateral Movement (AML.TA0015).
- v5.2.0 (January 2026) added AI Service API (AML.T0096) and the SesameOp case study (AML.CS0042).
- v5.3.0 (January 2026) added Deploy AI Agent (AML.T0103).
- v5.4.0 (February 2026) added Publish Poisoned AI Agent Tool (AML.T0104), Escape to Host (AML.T0105), and the OpenClaw case studies (AML.CS0050, AML.CS0051).

This mapping tracks against v5.4.0. Later ATLAS releases will shift specific cross-references.

## Mapping table

| EKC sub-technique | Description (abbreviated) | Relevant ATLAS tactic | Representative ATLAS techniques |
|---|---|---|---|
| EKC-0.1 | Training data poisoning | Resource Development; ML Attack Staging | Poison Training Data (AML.T0020); AI Supply Chain Compromise: Data |
| EKC-0.2 | Fine-tuning backdoor | Resource Development; ML Attack Staging | Backdoor ML Model (AML.T0018); Manipulate AI Model (AML.T0018) and sub-techniques |
| EKC-0.3 | Pre-trained model trojan | Resource Development | AI Supply Chain Compromise: AI Software (AML.T0010.001); related to PoisonGPT case study (AML.CS0019) |
| EKC-0.4 | Tokenizer or preprocessing manipulation | Resource Development | AI Supply Chain Compromise: Software (broader) |
| EKC-0.5 | Malicious MCP server or tool catalog entry | Resource Development | Publish Poisoned AI Agent Tool (AML.T0104, added v5.4.0); related case study AML.CS0049 (Supply Chain Compromise via Poisoned ClawdBot Skill) |
| EKC-1.1 | Model fingerprinting | Reconnaissance; Discovery | Active Scanning (AML.T0006); Discover ML Model Family / Ontology techniques |
| EKC-1.2 | System prompt enumeration | Discovery | Discover AI Agent Configuration (AML.T0084) and sub-techniques including Embedded Knowledge (AML.T0084.000) |
| EKC-1.3 | Capability and tool enumeration | Discovery | Discover AI Agent Configuration: Tool Definitions (AML.T0084.001); Cloud Service Discovery (AML.T0075) |
| EKC-1.4 | Guardrail mapping | Reconnaissance; Discovery | Search Open Websites/Domains (AML.T0095); Active Scanning (AML.T0006) |
| EKC-1.5 | Embedding or retrieval surface discovery | Discovery | Discover AI Agent Configuration (AML.T0084); Data from AI Services: RAG Databases (AML.T0085.000) |
| EKC-2.1 | Adversarial prompt crafting | ML Attack Staging | Craft Adversarial Data; LLM Prompt Obfuscation (AML.T0068) |
| EKC-2.2 | Multi-modal payload construction | ML Attack Staging | Craft Adversarial Data (multi-modal variants) |
| EKC-2.3 | Malicious tool or MCP package | Resource Development | Publish Poisoned AI Agent Tool (AML.T0104) |
| EKC-2.4 | Jailbreak chain assembly | ML Attack Staging | LLM Jailbreak (AML.T0054) |
| EKC-2.5 | AI-generated polymorphic malware | Resource Development | Obtain Capabilities: Generative AI (AML.T0016.002); Generate Malicious Commands (AML.T0102); cf. LAMEHUG case study (AML.CS0044) |
| EKC-3.1 | Indirect prompt injection via web | Initial Access; Execution | LLM Prompt Injection: Indirect (AML.T0051.001); Drive-by Compromise (AML.T0078) |
| EKC-3.2 | RAG corpus poisoning | Initial Access; Persistence | AI Agent Tool Data Poisoning (AML.T0099); RAG Credential Harvesting (AML.T0082) when used to seed retrievable content |
| EKC-3.3 | Email or message-borne injection | Initial Access | LLM Prompt Injection: Indirect (AML.T0051.001); Prompt Infiltration via Public-Facing Application (AML.T0093) |
| EKC-3.4 | Document-borne injection | Initial Access | LLM Prompt Injection: Indirect (AML.T0051.001) |
| EKC-3.5 | Tool-description poisoning | Initial Access; Resource Development | Publish Poisoned AI Agent Tool (AML.T0104) |
| EKC-3.6 | Image, audio, or QR-code injection | Initial Access | LLM Prompt Injection: Indirect (AML.T0051.001), multi-modal variants |
| EKC-4.1 | Direct prompt injection success | Execution | LLM Prompt Injection: Direct (AML.T0051.000) |
| EKC-4.2 | Indirect prompt injection success | Execution | LLM Prompt Injection: Indirect (AML.T0051.001); LLM Prompt Injection: Triggered (AML.T0051.002) |
| EKC-4.3 | Confused-deputy tool invocation | Execution | AI Agent Tool Invocation (AML.T0053); AI Agent Clickbait (AML.T0100) |
| EKC-4.4 | Guardrail or classifier bypass | Defense Evasion | LLM Jailbreak (AML.T0054); Evade AI Model (AML.T0015) |
| EKC-4.5 | Memory or context pollution | Persistence | AI Agent Context Poisoning (AML.T0080); AI Agent Context Poisoning: Memory (AML.T0080.001); Manipulate User LLM Chat History (AML.T0092) |
| EKC-5.1 | Persistent memory implant | Persistence | AI Agent Context Poisoning: Memory (AML.T0080.001); cf. case study Hacking ChatGPT's Memories with Prompt Injection (AML.CS0040) |
| EKC-5.2 | System prompt override | Persistence | Modify AI Agent Configuration (AML.T0081) |
| EKC-5.3 | Malicious connector installation | Persistence; Initial Access | Modify AI Agent Configuration (AML.T0081); Publish Poisoned AI Agent Tool (AML.T0104); Deploy AI Agent (AML.T0103) |
| EKC-5.4 | RAG corpus persistence | Persistence | AI Agent Tool Data Poisoning (AML.T0099) when seeded for re-retrieval; Delay Execution of LLM Instructions (AML.T0094) |
| EKC-5.5 | Stored skill or workflow contamination | Persistence | Modify AI Agent Configuration (AML.T0081); cf. case study AML.CS0049 |
| EKC-6.1 | LLM channel as C2 | Command and Control (AML.TA0014) | AI Service API (AML.T0096); cf. case study SesameOp (AML.CS0042); OpenClaw Command and Control via Prompt Injection (AML.CS0051) |
| EKC-6.2 | Memory-mediated C2 | Command and Control | AI Agent Context Poisoning: Memory (AML.T0080.001) used as a dead-drop |
| EKC-6.3 | RAG-mediated C2 | Command and Control | AI Agent Tool Data Poisoning (AML.T0099) used iteratively |
| EKC-6.4 | Tool-output C2 | Command and Control | AI Service API (AML.T0096); related to confused-deputy AI Agent Tool Invocation (AML.T0053) |
| EKC-6.5 | Cross-session steganographic C2 | Command and Control | LLM Prompt Obfuscation (AML.T0068); case study Planting Instructions for Delayed Automatic AI Agent Tool Invocation (AML.CS0038) |
| EKC-7a | Classical data exfiltration | Exfiltration; Impact | Exfiltration via AI Inference API (AML.T0024); Exfiltration via AI Agent Tool Invocation (AML.T0086); Data from AI Services (AML.T0085) |
| EKC-7b.1 | API-based model extraction | Exfiltration | Extract ML Model; Create Proxy ML Model |
| EKC-7b.2 | Training-data extraction | Exfiltration | Extract Training Data; Exfiltration via AI Inference API: Infer Training Data Membership (AML.T0024.000) |
| EKC-7b.3 | Membership inference | Exfiltration | Exfiltration via AI Inference API: Infer Training Data Membership (AML.T0024.000) |
| EKC-7b.4 | System prompt or instruction extraction | Exfiltration | Discover AI Agent Configuration (AML.T0084) used as exfiltration objective |
| EKC-7b.5 | Capability mining | Impact | LLM Jacking case study (AML.CS0029); ML-Enabled Product or Service abuse |
| EKC-7c.1 | Tool-mediated lateral action | Lateral Movement (AML.TA0015) | AI Agent Tool Invocation (AML.T0053); Exfiltration via AI Agent Tool Invocation (AML.T0086) |
| EKC-7c.2 | Cross-app pivot | Lateral Movement | Use Alternate Authentication Material (AML.T0091); AI Agent Tool Credential Harvesting (AML.T0098) |
| EKC-7c.3 | Identity confusion attack | Lateral Movement; Privilege Escalation | Use Alternate Authentication Material: Application Access Token (AML.T0091.000) |
| EKC-7c.4 | Recursive agent abuse | Lateral Movement | Deploy AI Agent (AML.T0103); AI Agent (AML.T0108, added v5.4.0) |
| EKC-7c.5 | Workflow weaponization | Lateral Movement; Impact | Modify AI Agent Configuration (AML.T0081); Data Destruction via AI Agent Tool Invocation (AML.T0101) |

## Notes on the mapping

The EKC puts agentic-pivot and memory-mediated C2 inside Stage 7c and Stage 6 (kill chain stages). ATLAS catalogs the same primitive techniques under its tactics matrix (Lateral Movement AML.TA0015, Command and Control AML.TA0014). Defenders who reason in kill-chain stages get the temporal view from the EKC. Defenders who reason in tactics matrices get the catalog view from ATLAS.

ATLAS technique IDs and names cited above come from official MITRE ATLAS release notes through v5.4.0. A small number of older ATLAS techniques (Extract ML Model, Craft Adversarial Data) appear in the public ATLAS matrix without specific ID confirmation in the release notes searched. See https://atlas.mitre.org for the authoritative current catalog.

ATLAS continues its monthly release cadence. Specific technique IDs and names will evolve. This mapping is refreshed with each EKC minor release.

For exhaustive technique-by-technique authoritative names and definitions, consult the official MITRE ATLAS website at https://atlas.mitre.org and the data repository at https://github.com/mitre-atlas/atlas-data.
