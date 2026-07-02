# Code Review and QA (Deprecated)

## Summary

Deprecated Skills OS v1 aggregate plugin retained as a transition marker while v2 reorganizes capabilities into plugin-first role packages.

The skills formerly contained here have moved into clearer v2 destinations. No symlinks or aliases are used.

## What this contains

### Moved skills

| Former skill | New plugin |
| --- | --- |
| `code-review` | [`vulnerability-focused-code-review`](../vulnerability-focused-code-review/) |
| `cpp-core-guidelines` | [`developer-code-review-and-qa`](../developer-code-review-and-qa/) |
| `webapp-qa` | [`developer-code-review-and-qa`](../developer-code-review-and-qa/) |

## Recommended agents

Use the recommended agents listed in the destination plugin and role READMEs. The former aggregate workflow commonly used:

- `code-reviewer`
- `qa-tester`

## Roadmap

### Near-term

- [x] Split the aggregate plugin into developer-focused and vulnerability-focused destinations.
- [ ] Decide when to remove or hide this deprecated plugin from marketplace/discovery plumbing.

### Mid-term

- [ ] Remove this transition marker after v2 consumers have moved to the split plugin names.
