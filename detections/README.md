# Example Sigma rules

These are **examples**. They show how EKC sub-technique IDs can be carried into detection content so that an alert, a hunt, and a threat report all point at the same stage. They have not been tuned against production telemetry. Expect to adjust field names, keywords and thresholds before you deploy any of them.

Every rule:

- has a title starting with `EKC Example` and a description starting with `EXAMPLE RULE.`
- is tagged with one or more `ekc.<id>` tags (`ekc.3.7` is EKC-3.7, `ekc.7c.6` is EKC-7c.6)
- uses `status: experimental`

`python tools/validate_sigma.py` parses every file with pySigma, runs pySigma's rule checks, and fails if a tag names an EKC ID that does not exist. CI runs it on every pull request.

## Rules

| File | EKC IDs | Log source | What it looks for |
|---|---|---|---|
| `ekc_0.5_mcp_tool_description_instructions.yml` | EKC-0.5, EKC-3.5 | `product: mcp` | Tool descriptions in `tools/list` responses that contain instructions aimed at the model |
| `ekc_1.6_agent_card_enumeration.yml` | EKC-1.6 | `category: webserver` | One client pulling A2A Agent Cards from many hosts (base rule plus a Sigma correlation rule) |
| `ekc_3.7_assistant_link_prefilled_memory_prompt.yml` | EKC-3.7, EKC-5.1 | `category: proxy` | Assistant URLs with a prefilled prompt that asks the assistant to remember a source as trusted |
| `ekc_3.8_unverified_agent_card.yml` | EKC-3.8 | `product: ai_agent` | Delegation to a peer whose Agent Card is unsigned, fails verification, or uses a new key |
| `ekc_4.6_computer_use_agent_local_navigation.yml` | EKC-4.6, EKC-3.9 | `product: ai_agent` | Browser or computer-use agents opening `file://`, loopback, metadata or private addresses |
| `ekc_5.6_shared_memory_write_untrusted_origin.yml` | EKC-5.6, EKC-6.2 | `product: ai_agent` | Writes to shared memory whose content came from retrieved data, a tool result, or a peer agent |
| `ekc_6.6_peer_agent_asks_for_client_context.yml` | EKC-6.6, EKC-1.2 | `product: ai_agent` | A remote agent asking the client agent for its instructions, tools, or history |
| `ekc_7c.6_agent_reads_credentials.yml` | EKC-7c.6 | `product: ai_agent` | Agent file reads of `/proc/self/environ`, cloud credential files, SSH keys, or agent config |
| `ekc_7c.6_mcp_token_audience_mismatch.yml` | EKC-7c.6, EKC-7c.3 | `product: mcp` | An MCP server receiving a token that was not issued to it (token passthrough) |

## Log sources and fields

Two of the rules use standard Sigma categories (`proxy`, `webserver`) and their usual field names. The rest use two generic log sources:

- `product: ai_agent`: telemetry from an agent runtime or agent framework (tool execution, memory operations, agent-to-agent delegation)
- `product: mcp`: telemetry from an MCP server, client, or gateway

Where a field already exists in the [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai), the rules use that name. Those conventions are still at `development` stability, so names can change; check them against the version your SDK emits. Fields the conventions do not cover yet use an `ekc.` prefix so it is obvious they are enrichment you have to add.

| Field | Origin | Meaning |
|---|---|---|
| `gen_ai.operation.name` | OTel GenAI | `execute_tool`, `invoke_agent`, `create_memory`, `update_memory`, `upsert_memory`, and others |
| `gen_ai.tool.name` | OTel GenAI | Name of the tool the agent called |
| `gen_ai.tool.call.arguments` | OTel GenAI | Tool call arguments. The conventions expect an object and mark it opt-in because it can hold sensitive data. The `contains` and `re` matches here assume your backend stores it as a string; adapt them if it keeps structured fields |
| `mcp.method.name` | OTel GenAI (MCP) | MCP JSON-RPC method, for example `tools/list` or `tools/call` |
| `ekc.tool.description` | EKC enrichment | Tool description from an MCP `tools/list` response, logged per tool by a gateway or client. OTel defines `gen_ai.tool.description` on tool-execution spans, not on `tools/list` |
| `ekc.content_origin` | EKC enrichment | Where the content behind an action came from: `user`, `retrieved_content`, `tool_result`, `peer_agent` |
| `ekc.memory_scope` | EKC enrichment | `user` for per-user memory, `shared` or `organization` for stores many principals read |
| `ekc.agent_card.signature_status` | EKC enrichment | Result of verifying the peer's Agent Card JWS: `valid`, `invalid`, `missing` |
| `ekc.agent_card.key_first_seen` | EKC enrichment | `true` the first time a signing key is seen for a given peer agent |
| `ekc.message.origin` / `ekc.message.text` | EKC enrichment | Sender role and text of an agent-to-agent message, logged on the client side |
| `ekc.token.audience_valid` | EKC enrichment | Result of the MCP server's token audience check |

`ekc.content_origin` is the field that makes most of these rules work, and it is also the one least likely to exist in your logs today. It is the logging side of the argument-lineage control in the README (Stage 4): if you cannot say where the text that drove a tool call came from, you cannot tell a user's request from an injected one.

## Converting

With [sigma-cli](https://github.com/SigmaHQ/sigma-cli), add a processing pipeline that maps the generic fields to your schema, then convert:

```bash
sigma convert -t splunk -p my_ai_agent_pipeline.yml detections/sigma/
```

The `proxy` and `webserver` rules work with the standard pipelines for most backends.
