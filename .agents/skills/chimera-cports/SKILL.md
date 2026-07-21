---
name: chimera-cports
description: Creates, updates, and debugs Chimera Linux cports package templates, including separately packaging missing dependencies and iterating until `./cbuild pkg user/<package>` succeeds. Use for Chimera package requests involving cports, cbuild, template.py, build styles, makedepends, subpackages, or package build failures.
---

# Chimera cports packaging

Create simple, policy-compliant source packages in the current cports checkout. Treat the checkout's documentation and existing templates as the current API; do not rely on remembered cbuild behavior.

## Policy gate

Read `CONTRIBUTING.md` first. It currently prohibits AI-prepared upstream contributions. Tell the user about this before editing package files. Proceed only for local/personal packaging, evaluation, or another use that does not misrepresent AI-generated work as an acceptable upstream contribution. Do not claim the result is eligible for submission.

## Workflow

1. **Load repository truth**
   - Read all of `CONTRIBUTING.md`, `Packaging.md`, and `README.md` from the repository root, in that order.
   - Follow documentation links needed for the task; read `Usage.md` before invoking or troubleshooting cbuild.
   - Check `git status --short` and preserve unrelated work.

2. **Research upstream and local precedent**
   - Establish the latest stable release, canonical homepage, source archive, SPDX license, build system, install behavior, test command, and complete dependency graph from authoritative upstream files.
   - Inspect the released source in `/tmp`; do not infer dependencies only from a project summary.
   - Find two or three nearby, recently maintained cports templates using the same build style or language. Prefer their current idioms over generic examples.
   - Use a stable release, not a VCS snapshot, unless the request explicitly justifies an exception.

3. **Resolve dependencies before authoring**
   - Check whether every direct build, host-tool, test, and explicit runtime dependency is already provided by `main` or `user`, including relevant `-devel` subpackages and automatic providers.
   - Classify runnable build-machine tools as `hostmakedepends`, target libraries/headers as `makedepends`, test-only requirements as `checkdepends`, and only non-scanned runtime requirements as `depends`.
   - Rely on cbuild's shared-library, pkg-config, command, and symlink scanners; do not duplicate automatic runtime dependencies.
   - Package each missing reusable dependency as its own `user/<dependency>` template first. Keep dependency templates separate from the requested package and ensure the graph is acyclic.
   - Vendor a dependency only when upstream requires a substantially outdated version or carries necessary modifications that are not viable against the packaged release. Verify that exception from lockfiles, patches, or upstream build logic and record a concise comment. Convenience, missing initial packaging, or build difficulty is not a vendoring justification.

4. **Write the smallest correct template**
   - Create `user/<pkgname>/template.py`; package names are lowercase and normally follow upstream.
   - Use the matching cbuild `build_style` and declarative variables. Override only phases the style cannot express.
   - Fill metadata from verified sources: `pkgver`, initial `pkgrel = 0`, concise American-English `pkgdesc`, SPDX `license`, canonical `url`, stable `source`, and independently verified `sha256`.
   - Use `/usr/bin`, `/usr/lib`, `/usr/include`, and `/usr/share`; never emit `/usr/sbin`, `/usr/lib64`, top-level `/bin` or `/lib`, or packaged `/var` state.
   - Install required custom licenses with `self.install_license`. Put examples under `/usr/share/examples/<pkgname>` where appropriate. Mark legitimate `/etc` contents with `etcfiles`; prefer immutable defaults and tmpfiles/sysusers mechanisms.
   - Let automatic subpackages handle docs, manuals, services, completions, locales, debug data, and static libraries. Add a `-devel` subpackage for libraries and use `return self.default_devel()` unless the contents require a narrower split. Run `./cbuild relink-subpkgs user/<pkgname>` after adding explicit subpackages.
   - Preserve cross compilation. Never assume native architecture, replace cbuild flags, download during configure/build/check/install, patch source with ad-hoc `sed`, or retain in-memory state between resumable phases.
   - Keep tests enabled. If tests cannot run because of a reproducible technical constraint or dependency cycle, still define the check path where useful, set `!check`, and place a specific reason immediately above `options`.
   - Add narrowly scoped patches under `patches/` rather than source-edit commands, and make fixes suitable for upstreaming.
   - Format as Black-compatible Python with the repository's field ordering and 80-column style.

   Read `references/template-examples.md` when choosing template structure, dependency handling, or correcting common anti-patterns.

5. **Validate and repair**
   - Run `./cbuild lint user/<pkgname>` after each template is structurally complete; fix all errors.
   - Ensure cbuild prerequisites from `Usage.md` exist. If signing keys or the build root are missing, report the exact setup command (`./cbuild keygen` or `./cbuild bootstrap`) rather than bypassing the requirement.
   - Build separately packaged dependencies first when useful for diagnosis, then run the required acceptance command exactly:

     ```sh
     ./cbuild pkg user/<pkgname>
     ```

   - On failure, read the complete relevant cbuild log, identify the first root cause, and fix the template, patch, or separate dependency. Re-run the same command until it exits successfully.
   - Do not use `--no-depends-check`, `--dirty-build`, `--skip-check`, `!check`, disabled hardening, disabled cross support, or vendoring merely to make the build green. Such changes require an independently verified package constraint and a precise comment.
   - After success, inspect package contents and generated dependency metadata for misplaced files, accidental vendoring, missing subpackages, and undeclared runtime data. Run `./cbuild cycle-check user/<pkgname>` when new dependency templates were added.
   - If a blocker is external or environmental, stop with the failing command, relevant log excerpt, diagnosis, and the smallest user action needed. Never report a failed or skipped build as complete.

## Completion report

Report:

- templates and auxiliary files created or changed
- separately packaged dependencies and why each was needed
- lint, cycle-check, and `./cbuild pkg user/<pkgname>` results
- tests run or the documented reason they cannot run
- remaining policy, architecture, licensing, or environment limitations
