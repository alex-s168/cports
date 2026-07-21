# Chimera cports Skill Specification

## Intent

Guide an agent from upstream inspection through a policy-compliant Chimera Linux cports template that builds successfully. Optimize for small declarative templates, separately packaged reusable dependencies, and honest build verification.

## Scope

In scope:
- new and updated `template.py` files
- missing dependency templates
- patches, files, and explicit subpackages
- cbuild lint, dependency, and package-build diagnosis

Out of scope:
- disguising AI-generated work as acceptable upstream contributions
- binary repackaging when a viable source build exists
- bypassing cbuild policy or environment requirements
- changing cbuild itself

## Users And Trigger Context

- Primary users: people maintaining local Chimera cports packages
- Common requests: package an upstream release, fix a template, add a missing dependency, or make `./cbuild pkg user/x` pass
- Should not trigger for: unrelated Linux package formats, ordinary Python packaging, or general build-system help without Chimera cports

## Runtime Contract

- Required first actions: read repository policy/manual docs and warn about the current AI-contribution prohibition
- Required outputs: package templates, separately packaged reusable dependencies, and validation evidence
- Non-negotiable constraints: final `./cbuild pkg user/<package>` succeeds or the agent reports an unresolved blocker; no dependency vendoring except verified outdated/modified-version requirements
- Expected bundled files loaded at runtime: `references/template-examples.md` when selecting or repairing template structure

## Source And Evidence Model

Authoritative sources:
- repository `CONTRIBUTING.md`, `Packaging.md`, `README.md`, and `Usage.md`
- released upstream source metadata and build files
- current nearby cports templates and cbuild build styles

Useful improvement sources:
- cbuild failure logs
- package review feedback and repository history
- working and rejected templates

Do not store secrets, signing keys, private URLs, or unrelated user data.

## Reference Architecture

- `SKILL.md` contains the mandatory workflow and validation loop
- `references/` contains focused transformed template examples
- `SOURCES.md` contains provenance, design decisions, coverage, and gaps
- no scripts or assets are currently needed

## Validation

- Lightweight validation: Agent Skills structural validator and manual reference-link review
- Runtime validation: `./cbuild lint`, optional cycle check, and exact final package command
- Acceptance gates: valid skill structure; runtime workflow never claims completion after a failed/skipped build

## Known Limitations

- Packaging details change with the cports checkout; repository docs must be reread on every invocation
- Full architecture coverage may require builders unavailable in the local environment
- The current upstream policy rejects AI-prepared contributions

## Maintenance Notes

- Update `SKILL.md` when cports policy, dependency rules, or validation commands change
- Update `SOURCES.md` when source coverage or design decisions change
- Add evidence examples only when concrete outcomes expose a recurring behavior gap
