# MythicMCP setup and tool surface

Source: `blaisebits/mythicmcp` (`MythicMCP`), a Python 3.10+ MCP server for Mythic C2 that exposes operations, callbacks, tasks, files, payloads, C2 profiles, generic callback command execution, and bundled typed Apollo/Poseidon/Arachne toolsets.

## Install / update

```bash
uv tool install git+https://github.com/blaisebits/mythicmcp
uv tool install --upgrade git+https://github.com/blaisebits/mythicmcp
mythicmcp --help
```

For source checkout development:

```bash
git clone https://github.com/blaisebits/mythicmcp /opt/mythicmcp
cd /opt/mythicmcp
uv sync --all-extras
uv run pytest tests/unit -q
```

## Codex MCP configuration

Installed command:

```toml
[mcp_servers.mythicmcp]
command = "mythicmcp"
args = []

[mcp_servers.mythicmcp.env]
MYTHIC_SERVER_URL = "https://mythic.local:7443"
MYTHIC_API_TOKEN = "YOUR_TOKEN"
MYTHIC_TIMEOUT = "60"
MYTHIC_AGENTS = "apollo,poseidon"
MYTHIC_HOTLOAD = "1"
```

Source checkout command:

```toml
[mcp_servers.mythicmcp]
command = "uv"
args = ["run", "--directory", "/opt/mythicmcp", "mythicmcp"]

[mcp_servers.mythicmcp.env]
MYTHIC_SERVER_URL = "https://mythic.local:7443"
MYTHIC_API_TOKEN = "YOUR_TOKEN"
```

Username/password auth can replace token auth with `MYTHIC_USERNAME` and `MYTHIC_PASSWORD`. Keep secrets in local config or environment, not repository files.

## Core tools

Connection / operation:

- `core_check_connection`
- `core_list_operations`
- `core_set_operation(operation_id)`
- `core_get_operation(operation_id?)`

Callbacks / commands / tasks:

- `core_list_callbacks`
- `core_get_callback(callback_id)`
- `core_list_callback_commands(callback_id, source="")`
- `core_get_callback_command(callback_id, command_name, source="")`
- `core_execute_callback_command(callback_id, command_name, arguments, source="", timeout?)`
- `core_list_callback_tasks(callback_id)`
- `core_get_task_output(task_display_id)`
- `core_get_task_callback(task_display_id)`
- `core_list_interactive_tasks(parent_task_display_id)`
- `core_get_interactive_session(parent_task_display_id)`

File browser / files:

- `core_get_file_browser_by_task(task_display_id)`
- `core_list_file_browser(host, path="")`
- `core_upload_file(filename?, content?, file_path?)`
- `core_download_file(file_uuid)`
- `core_list_downloaded_files`
- `core_list_uploaded_files`

C2 profiles:

- `core_list_c2_profiles`
- `core_get_c2_profile_parameters(c2_profile_name)`
- `core_create_c2_instance(instance_name, c2_profile_name, c2_parameters)`
- `core_list_c2_instances`
- `core_get_c2_instance(instance_name, c2_profile_name)`
- `core_delete_c2_instance(instance_name, c2_profile_name)`

Payloads:

- `core_list_payloads`
- `core_get_payload(payload_uuid)`
- `core_create_payload(payload_type_name, filename, operating_system, c2_profiles?, c2_instances?, description?, commands?, build_parameters?, include_all_commands?, timeout?)`
- `core_download_payload(payload_uuid)`
- `core_delete_payload(payload_uuid)`
- `core_check_payload_config(payload_uuid)`
- `core_payload_redirect_rules(payload_uuid)`

Plugins / typed agents:

- `core_list_plugins`
- `list_available_agents`
- `load_agent_tools(agent_name)` when `MYTHIC_HOTLOAD=1`
- `unload_agent_tools(agent_name)` when `MYTHIC_HOTLOAD=1`

Resource:

- `mythic://docs/usage-patterns` contains the server's command-execution guidance; read it when command arguments are ambiguous.

## Troubleshooting

- `MYTHIC_SERVER_URL is required`: set the env var in Codex MCP config, not only the shell.
- `Either MYTHIC_API_TOKEN or both MYTHIC_USERNAME and MYTHIC_PASSWORD are required`: add token or username/password auth.
- Tools missing after config changes: restart Codex, check `/mcp`, and run `mythicmcp --help` in the same environment.
- Command timeout: use task output and task status to distinguish slow execution from failure.
- Command argument mismatch: inspect `argument_mode`, `execution_usage`, and `example_arguments`; `usage` may be display text only.
