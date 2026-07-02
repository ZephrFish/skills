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
