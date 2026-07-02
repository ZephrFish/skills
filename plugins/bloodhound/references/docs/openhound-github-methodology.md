# OpenHound GitHub Methodology

Use for OpenHound GitHub OpenGraph analysis with OpenHound GitHub-collected data.

## Collector context

- OpenHound GitHub models GitHub organizations, users, teams, repositories, branch protections, workflows, Actions settings, secrets/variables metadata, apps, personal access tokens, and external identity relationships.
- Use `references/examples/openhound-github/samples/` only for small legacy SAML/SCIM payload examples when sidecar shape matters; prefer the OpenHound GitHub repository descriptions and saved searches for current schema/query shape.
- Confirm org/repository collection coverage before treating missing controls, users, teams, or settings as absent.

## Focus areas

- Organization and repository permission inheritance: owners, teams, org roles, repo roles, base roles, custom roles, and outside collaborators.
- High-risk repository control: admin/write access, protected branch bypass, default branch force-push/delete settings, CODEOWNERS gaps, and pull-request review bypass.
- GitHub Actions and secrets: Actions policy, allowed actions, SHA pinning, environment protection, organization/repository/environment secrets and variables.
- Cloud pivots: GitHub OIDC/federated identity relationships into Azure or other cloud identities.
- Hybrid identity: SSO links from Okta/Azure/SCIM users into GitHub users, external identities without SCIM, and privileged GitHub users linked to identity-provider accounts.

## Query guidance

- OpenHound GitHub labels and relationships generally use `GH_` prefixes.
- Read `../examples/node-edge-reference.md` before inventing GitHub labels or edges.
- Read `scim-methodology.md` before interpreting external identity or SCIM bridge paths.
- Favor saved-search patterns for branch protection, app installations, external identities, secrets, PATs, and OIDC federation.
- Return paths for permission inheritance and tables for posture checks.
- When describing secret risk, distinguish existence/scope metadata from cleartext secret access.
- Confirm whether the org has app, Actions, SAML, and SCIM collection coverage before concluding that a control is absent.

## Good starting points

- Query index: `../query-indexes/openhound-github.md`
- Query snapshots: `../query-snapshots/openhound-github/saved-searches/`
- Example Cypher: `../examples/example-cypher.md`
- Node/edge reference: `../examples/node-edge-reference.md`
- Collector source index: `collector-source-index.md`
- Official OpenHound GitHub query docs: https://bloodhound.specterops.io/opengraph/extensions/github/queries
- OpenHound GitHub repository: https://github.com/SpecterOps/openhound-github
