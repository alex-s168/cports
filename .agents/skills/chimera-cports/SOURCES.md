# Sources and synthesis

## Classification

- Skill class: `workflow-process`
- Primary shape: `inline-guidance`
- Secondary mechanics: fixed ordered steps and validate-fix-repeat loop
- Simplicity rationale: one dominant packaging path fits in `SKILL.md`; scripts, routing, and provider-specific mechanics would add ceremony without improving cbuild outcomes
- Portability: Agent Skills-compatible and provider-neutral

## Source inventory

| Source | Trust | Contribution | Constraints |
|---|---|---|---|
| `CONTRIBUTING.md` | authoritative | contribution policy, style, build responsibility | Current policy prohibits AI-prepared submissions |
| `Packaging.md` | authoritative | template API, dependency classes, build styles, filesystem, hardening, checks, subpackages | Must be reread because it defines the supported API |
| `README.md` | authoritative | document routing and repository context | Points packagers to Packaging and Usage |
| `Usage.md` | authoritative | prerequisites, bootstrap, lint/build commands, failure-related flags | Environment-specific setup may block local builds |
| Current `user/*/template.py` examples | strong local precedent | field order and current build-style idioms | Examples are precedents, not policy |
| Pi `docs/skills.md` | authoritative for harness | project skill path, format, discovery, validation | No extra registration catalog exists here |
| `skill-writer` guidance | authoritative local method | synthesis, authoring, trigger, SPEC, and validation requirements | Maintenance-only content stays out of runtime guidance |

## Decisions

- Adopted: put the project skill at `.agents/skills/chimera-cports/`, the documented default when no repository convention exists.
- Adopted: warn and gate on `CONTRIBUTING.md` before edits; the skill must not conceal the repository's AI policy.
- Adopted: package every missing reusable dependency separately, except a verified substantially outdated or modified upstream requirement.
- Adopted: require the exact final command `./cbuild pkg user/<pkgname>` and a repair loop.
- Adopted: include a routed example reference because concrete generator examples are useful but not required in every runtime step.
- Rejected: bundled cbuild wrapper/validator script; cbuild itself is the authoritative validator.
- Rejected: copying the full packaging manual into the skill; runtime instructions require fresh repository docs.
- Deferred: architecture matrix builds, because local builders and emulation availability vary.

## Coverage matrix

| Dimension | Status | Coverage |
|---|---|---|
| Preconditions | covered | repository docs, git state, cbuild setup |
| Ordered flow | covered | policy → research → dependencies → template → validate |
| Failure handling | covered | first-root-cause log diagnosis and retry loop |
| Safety boundaries | covered | preserve user work, no bypass flags, no false success |
| Dependency policy | covered | classes, scanners, separate packages, narrow exception |
| Output acceptance | covered | lint, cycle check when relevant, exact package build |
| Happy-path example | covered | Meson library template |
| Robust example | covered | separately packaged missing dependency |
| Negative/repair example | covered | vendoring/disabled-check/source-mutation correction |

## Source adaptation

- Source intent: enforce Chimera's supported packaging API and quality expectations.
- Local target: an executable agent workflow for local cports package authoring.
- Fidelity boundary: retain policy, dependency, filesystem, build, and validation requirements.
- Local replacement: replace long narrative API prose with decisions, gates, and commands; require agents to reread source docs.
- Omitted: exhaustive variable/API descriptions, bootstrap internals, and contribution mechanics not needed during package authoring.
- Rights/attribution: repository documentation is referenced by path; no substantial prose is copied.

## Trigger checks

Should trigger:
- "Package this release for Chimera Linux cports"
- "Create user/foo/template.py and make cbuild pass"
- "Fix the makedepends in this Chimera cport"
- "Package foo and its missing dependencies separately"

Should not trigger:
- "Write a Debian control file"
- "Publish my Python project to PyPI"
- "Debug a generic CMake build outside cports"
- "Explain how apk installs packages"

## Gaps and stopping rationale

No high-impact source gap is open. Architecture-wide validation depends on available builders and remains a runtime limitation. Collection stopped after authoritative policy/API/usage documents and representative current templates covered the happy path, dependency handling, failure recovery, and validation; more template sampling was low yield.
