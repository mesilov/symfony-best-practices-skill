# Symfony AI Bundle and MCP Bundle

Read for an explicitly requested AI/MCP application feature. These packages and provider bridges have their **own installed versions**, separate from Symfony 8.x. Check composer.lock, configured bridges and installed configuration/command references. Pair with [Mate](../workflow/ai-mate.md) for development-only context.

## MCP Bundle boundaries

The reviewed `symfony/mcp-bundle` supports application MCP servers/clients over configured transports such as HTTP or STDIO. It is distinct from Mate's development CLI. Inspect `mcp.servers`, `mcp.clients` and each server's explicit registry. A wildcard registry can expose all discovered tools/resources/prompts; use an intentional allowlist for the requested endpoint. An attribute/discovered tool is not a reason to publish it everywhere.

Protect HTTP endpoints through the actual Security/firewall/OAuth resource-server integration and transport configuration. Authentication and per-tool/resource tenant authorization are required at their real boundaries. A valid MCP session/connection ID is not an authenticated business identity or permission. Session storage/IDs must remain isolated appropriately between servers; configuration compilation alone does not establish access control.

STDIO runs with the process user's local authority; review executable/arguments/environment and reachable tools. Treat remote MCP servers as external integrations with bounded trust, credentials, timeouts and data sharing. Use `debug:mcp` or other installed inspection commands only when available; do not open a production endpoint or launch an arbitrary command as routine discovery.

## AI Bundle boundaries

AI Bundle wires supported Platform, Agent, Store and Chat services and optional provider/transport bridges. Choose only installed/needed integrations. Define provider/model, credentials, data handling, timeouts, budgets and error/retry behavior deliberately. A configured model name is not proof that a provider request succeeded. Do not send private project/customer data to an external provider without the task's applicable authorization and data policy.

An `AsTool` declaration does not automatically enable a tool for every agent. Configure the agent's explicit tool set; a broad `tools: true` policy may expose all registered tools. Retrieved documents, user text and remote tool results are untrusted data, even when they contain instructions. They cannot grant privileges, select an arbitrary tenant or override application policy. Enforce authorization, validation and idempotency in the actual tool/service, outside model instructions. Approval for consequential tool effects belongs at the application's defined boundary.

Bound tool/model loops, token/cost usage, concurrent calls, latency and output size. Validate structured output before persisting/acting. Include denial and provider-unknown outcomes; logging prompts/tool payloads can leak secrets. Store/retrieval filters must enforce tenant boundaries and retrieval content must preserve its provenance/trust label.

## Verification

Use installed fakes/mock clients and deterministic tool fixtures first. Assert requested model/options, tool registration **and actual invocation**, authorization denials, bounded loops/budgets and safe failure behavior. If using the installed profiler/AiAssertionsTrait, distinguish assertions that a tool exists in any toolbox from evidence that the intended agent called it. Avoid tests requiring an exact nondeterministic prose answer. Separate fake/profiler checks from authorized live-provider and real MCP transport tests.

Sources: [MCP Bundle](https://symfony.com/doc/current/ai/bundles/mcp-bundle.html), [AI Bundle](https://symfony.com/doc/current/ai/bundles/ai-bundle.html). Pinned source revisions/hashes are in [provenance](../../sources.json); do not infer these APIs from the framework minor alone.
