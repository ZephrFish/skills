---
name: mythic-mcp
description: Use MythicMCP from Codex to operate Mythic C2 through MCP tools. Use when configuring the blaisebits/mythicmcp server, checking Mythic connectivity, selecting operations, listing callbacks/tasks/files/payloads/C2 profiles, executing callback commands, creating payloads, using Apollo/Poseidon/Arachne typed tools, or troubleshooting Mythic MCP tool behavior.
---

# Mythic MCP

## Scope

Use this skill when Codex should drive an existing Mythic server through the `mythicmcp` MCP server rather than editing Mythic agent/profile source code.

Use `$mythic-implant-development` for payload type or implant implementation, `$mythic-profiles` for C2 profile/listener development, and `$mythic-translation-containers` for translation-container work.

## Setup check

If the Mythic MCP tools are not available in the active tool list, help configure Codex instead of inventing tool output. Read `references/mythicmcp-setup-and-tools.md` when setup, installation, exact tool names, or troubleshooting details are needed.

Minimum Codex config shape:

```toml
[mcp_servers.mythicmcp]
command = "mythicmcp"
args = []

[mcp_servers.mythicmcp.env]
MYTHIC_SERVER_URL = "https://mythic.local:7443"
MYTHIC_API_TOKEN = "YOUR_TOKEN"
# or MYTHIC_USERNAME / MYTHIC_PASSWORD
```

Restart Codex after MCP config changes and confirm the server appears under `/mcp` before relying on it.

## Operator workflow

1. **Establish context**
   - Call `core_check_connection` first; note authenticated user and current operation.
   - If no operation is selected, call `core_list_operations`, choose the requested operation, then `core_set_operation`.
   - Never print API tokens, passwords, full bearer headers, or downloaded sensitive file contents unless explicitly requested for evidence handling.

2. **Inventory access**
   - Use `core_list_callbacks` for the operation overview.
   - Use `core_get_callback` before tasking a callback; capture `callback_id` as canonical and treat `display_id` as UI-only.
   - Use task/file-browser tools to understand recent operator actions before repeating potentially noisy commands.

3. **Execute callback commands**
   - Use `core_list_callback_commands(callback_id)` to discover loaded commands.
   - Use `core_get_callback_command(callback_id, command_name, source="")` before execution.
   - Build `core_execute_callback_command` arguments from `argument_mode`, `execution_usage`, and `example_arguments`; prefer those over display-only `usage`.
   - For zero-arg commands, pass an empty string. For structured commands, pass a JSON object string matching the command metadata.
   - If execution times out but returns or implies a task ID, inspect `core_get_task_output` before deciding it failed.

4. **Files, payloads, and C2 profiles**
   - Upload tasking files with `core_upload_file`; download by UUID with `core_download_file` and summarize where saved.
   - Build payloads with `core_create_payload` only after validating payload type, OS, selected commands, build parameters, and C2 profile/instance values.
   - Use `core_check_payload_config` and `core_payload_redirect_rules` to validate egress assumptions before delivery.
   - Confirm before destructive actions such as `core_delete_payload` or `core_delete_c2_instance` unless the user explicitly requested cleanup.

5. **Agent-specific tools**
   - Use generic callback command tools for unsupported or unfamiliar agents.
   - If `MYTHIC_HOTLOAD=1` is enabled, use `list_available_agents`, `load_agent_tools`, and `unload_agent_tools` for typed Apollo, Poseidon, Arachne, or external YAML-driven agent tools.
   - Prefer typed tools only when their schema is clearer than generic command execution.

## Output requirements

For Mythic MCP operation tasks, return concise evidence:

- Mythic operation and authenticated context checked
- callback IDs / payload UUIDs / task display IDs used
- commands or MCP tools called, with important arguments redacted as needed
- task status and summarized output
- files created/downloaded and local paths when applicable
- assumptions, failures, and next recommended operator action
