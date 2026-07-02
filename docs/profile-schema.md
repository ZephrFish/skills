# Profile Schema

Profiles are declarative TOML manifests. Opening a profile file must not install anything. Installation requires an explicit installer command.

Final v2 planning shape:

```toml
schema_version = "0.1"
name = "research"
display_name = "Research"
description = "Short human-readable profile description."
status = "draft"

[profile]
inherits = ["base"]

[plugins]
required = []

[agents]
optional = []
```

Rules:

- Base uses `inherits = []`.
- Role profiles use `inherits = ["base"]`.
- Profiles list required plugins only.
- Profiles do not enumerate individual skills.
- All agents are optional.
- No `[install]`, `[ownership]`, `[docs]`, `kind`, `roles`, `workflows`, or `scripts` sections.

## Installer behavior

The role/profile installer consumes this schema directly:

```bash
uv run scripts/skills-os.py install research
```

Installer rules:

- Resolve `[profile].inherits` before installing plugins.
- Install only `[plugins].required`; profiles do not install individual skills.
- Treat `[agents].optional` as recommendations for the checkbox selector.
- Leave recommended agents unchecked by default; install only agents selected by the user or passed through explicit flags.
- Register selected agents in Codex config after copying their TOML files to the configured agent directory.
