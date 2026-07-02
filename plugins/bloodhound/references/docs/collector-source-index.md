# Collector Source Index

Use this index to identify collector outputs, upstream examples, and local references before writing BloodHound/OpenGraph analysis guidance.

## OpenHound GitHub

- Repository: https://github.com/SpecterOps/openhound-github
- Local saved searches: `references/query-snapshots/openhound-github/saved-searches/`
- Local query index: `references/query-indexes/openhound-github.md`
- Local small legacy SAML/SCIM samples:
  - `references/examples/openhound-github/samples/openhound_github_saml_O_kgDOCoV2OQ.json`
  - `references/examples/openhound-github/samples/openhound_github_scim_O_kgDOCoV2OQ.json`
- Upstream saved searches: `extension/saved_searches/`
- Upstream node docs: https://github.com/SpecterOps/openhound-github/tree/main/descriptions/nodes
- Upstream edge docs: https://github.com/SpecterOps/openhound-github/tree/main/descriptions/edges
- Useful upstream docs: `README.md`, `extension.yaml`, `docs/og-docs.json`, `descriptions/nodes/`, `descriptions/edges/`, `extension/privilege_zone_rules/`, and `extension/saved_searches/`.

## JamfHound / OpenHound Jamf

- Repository: https://github.com/SpecterOps/JamfHound
- Local saved searches: `references/query-snapshots/openhound-jamf/saved-searches/`
- Local query index: `references/query-indexes/openhound-jamf.md`
- Local schema examples: `references/examples/jamfhound/schema/`
- Local object examples: `references/examples/jamfhound/objects/`
- Upstream examples: `schema/`, `objects/`, and `snippets/` in the JamfHound repository.
- Use the local examples for Jamf Pro object shape and schema expectations; use saved-search snapshots for actual path queries.

## OktaHound / OpenHound Okta

- Repository: https://github.com/SpecterOps/OktaHound
- Local saved searches: `references/query-snapshots/openhound-okta/saved-searches/`
- Local query index: `references/query-indexes/openhound-okta.md`
- Useful upstream files: `README.md`, `Roadmap.md`, `Src/SpecterOps.OktaHound/okta.sample.oauth.yaml`, `Src/SpecterOps.OktaHound/okta.sample.token.yaml`, and model classes under `Src/SpecterOps.OktaHound/Model/`.
- Current local references do not vendor generated OktaHound sample data because the upstream repository exposes model/config examples rather than compact generated graph samples.

## SCIM

- Official overview: https://bloodhound.specterops.io/opengraph/extensions/scim/overview
- Official schema: https://bloodhound.specterops.io/opengraph/extensions/scim/schema
- Extension schema repo: https://github.com/SpecterOps/bloodhound-scim-extension
- Local methodology: `references/docs/scim-methodology.md`

## OpenGraph management

- Official management docs: https://bloodhound.specterops.io/opengraph/extensions/manage
- Local methodology: `references/docs/opengraph-extension-management.md`
