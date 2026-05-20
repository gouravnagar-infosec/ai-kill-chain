# EKC and OWASP Top 10 for LLM Applications (2025) mapping

Cross-references between the OWASP Top 10 for LLM Applications (2025 edition) and Extended Cyber Kill Chain stages.

## Relationship

OWASP organizes its content as a risk-prioritization list for application builders. The EKC organizes the same content as a temporal attack sequence for defender teams. Each OWASP category maps to one or more EKC stages where the underlying vulnerability is exploited. This mapping is one-to-many in both directions.

## Mapping table

| OWASP ID | OWASP risk name | Primary EKC stages | Notes |
|---|---|---|---|
| LLM01 | Prompt Injection | Stages 3, 4 (also 5, 6 for persistence and C2) | Direct injection lives in Stage 4. Indirect injection straddles Stage 3 (Delivery) and Stage 4 (Exploitation). Injection used to write to memory pollutes into Stage 5. Injection through RAG used as a recurring channel is Stage 6 C2. |
| LLM02 | Sensitive Information Disclosure | Stages 7a, 7b | Output-side leakage of training data, system prompts, or credentials is exfiltration. When the information class is the model itself, it is 7b model extraction. |
| LLM03 | Supply Chain | Stage 0 | This is the EKC pre-attack stage. |
| LLM04 | Data and Model Poisoning | Stage 0 (training-time) and Stage 5 (persistence-time, RAG corpus poisoning) | Poisoning that affects the model before deployment is Stage 0. Poisoning that affects an already-deployed RAG corpus is Stage 5 persistence. |
| LLM05 | Improper Output Handling | Stage 7c (Agentic Pivot) | When tool inputs or downstream-system inputs are taken from raw LLM output without sanitization, the LLM becomes a confused deputy invoking lateral actions. |
| LLM06 | Excessive Agency | Stage 7c (Agentic Pivot) | The agency-permission gap is the structural precondition for agentic pivot. Over-broad tool permissions amplify the blast radius of Stage 4 exploitation. |
| LLM07 | System Prompt Leakage | Stages 1 (Reconnaissance) and 7b (Exfiltration) | Used as a precursor to map the policy boundary: Stage 1. When the system prompt itself is the target of exfiltration: Stage 7b. |
| LLM08 | Vector and Embedding Weaknesses | Stages 3 (RAG poisoning) and 5 (RAG persistence) | The same RAG mechanism appears at both stages depending on whether the attacker is injecting fresh content or holding poisoned content across re-indexing. |
| LLM09 | Misinformation | Stage 7a (Impact variant) | The downstream impact stage. Cross-references to Stage 4 when the misinformation is induced by adversarial input rather than spontaneous hallucination. |
| LLM10 | Unbounded Consumption | Stages 7a (cost-impact) and 7b (extraction queries at scale) | High-volume programmatic queries map to either resource-exhaustion impact or to model-extraction objective depending on the adversary's goal. |

## Reading the mapping

For a SOC or detection engineering team that already uses the kill-chain framing, this mapping converts OWASP's vulnerability-class taxonomy into a stage-by-stage operational view.

"We have controls for LLM01 prompt injection" becomes a question about *which* stages of the kill chain those controls cover. Most prompt-injection controls operate at Stage 3 (input filtering) or Stage 4 (output guarding). Few operate at Stage 5 (memory-write guards) or Stage 6 (channel analysis). Those are exactly the stages where injection-mediated persistence and C2 escape the typical control set.

"We have controls for LLM06 excessive agency" becomes a question about whether the control reduces Stage 7c blast radius (per-tool permissions, human-in-loop) or only constrains Stage 4 invocation (refusal policies).

The kill-chain view exposes coverage gaps that the risk-list view does not.
