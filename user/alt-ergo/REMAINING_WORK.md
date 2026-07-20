# Remaining Work: OCaml Dependency Chain for alt-ergo

## Status: COMPLETED — all packages build successfully

The alt-ergo 2.6.3 package template at `user/alt-ergo/template.py` now builds
successfully. All dependencies through Tier 6 are complete and the package
produces: `alt-ergo`, `alt-ergo-lib`, `alt-ergo-parsers`.

## Build Order (final)

```
Tier 0 (pre-built in Chimera repos): dune, cmdliner, sexplib0, ppx-derivers, cppo
Tier 1: ocamlbuild ✓
Tier 2: logs-ocaml, fmt-ocaml, zarith ✓
  + extras: stdlib-shims, ocaml-compiler-libs-janestreet, hmap
Tier 3: ocplib-simplex, dolmen, menhir ✓
  + extras: dune-private-libs, dune-site, dune-build-info
Tier 4: ppxlib, psmt2-frontend ✓
Tier 5: ppx-blob, ppx-deriving ✓
Tier 5b (new — dolmen sub-library deps): uutf, spelll, gen, pp-loc, seq ✓
Tier 6: dolmen (multi-package), alt-ergo ✓
```

## Packages Created

| Package | Version | Build | Purpose |
|---------|---------|-------|---------|
| `user/uutf` | 1.0.4 | ocamlbuild | UTF codec → dolmen_type |
| `user/spelll` | 0.4 | dune | Fuzzy search → dolmen_type |
| `user/gen` | 1.1 | dune | Iterators → dolmen_loop |
| `user/pp-loc` | 2.1.0 | dune | Source locations → dolmen_loop |
| `user/seq` | 0.3.1 | dune | Iterator compatibility → transitive dep |

## Packages Modified

### Install method fixes (default dune install broken)

The Chimera dune build_style's default `install()` uses `--create-install-files`
which produces incomplete `.install` files. Fixed by overriding `install()` to
call `dune install` directly with `--libdir /usr/lib` and without
`--create-install-files`:

| Package | Change |
|---------|--------|
| `user/dolmen` (pkgrel 1) | Multi-package build: `dolmen,dolmen_type,dolmen_loop`. Added subpackages `dolmen-type`, `dolmen-loop`. New deps: spelll, uutf, gen, pp-loc, seq, stdlib-shims. |
| `user/ocplib-simplex` (pkgrel 1) | Custom install, `!lintstatic` |
| `user/psmt2-frontend` (pkgrel 1) | Custom install, `!lintstatic` |
| `user/camlzip` (pkgrel 2) | Switched from dune to makefile build. Manual file install. |

### `.a` archive generation

OCaml packages using `ocamlbuild` do not produce `.a` static archives needed
for native linking. Fixed by running `ar rcs` during install:

| Package | Change |
|---------|--------|
| `user/fmt-ocaml` (pkgrel 1) | Added `ar rcs` for `fmt.a`, `fmt_tty.a` |
| `user/logs-ocaml` (pkgrel 1) | Added `ar rcs` for `logs.a`, `logs_fmt.a` |

### alt-ergo template evolution

`user/alt-ergo/template.py` accumulated these changes:
- Added `dolmen-type`, `dolmen-loop` (dolmen sub-library packages)
- Added `seq`, `stdlib-shims` (transitive dune dependencies)
- Added `fmt-ocaml-devel-static`, `logs-ocaml-devel`, `logs-ocaml-devel-static`
- Added `gmp-devel`, `gmp-devel-static` (for zarith native linking)
- Added `zlib-ng-compat-devel` (for camlzip native linking)
- Added `--mandir /usr/share/man` to dune install args (lint fix)
- Added `!check` (tests require qcheck, not packaged)
- Fixed subpackage paths from `usr/lib/ocaml/...` to `usr/lib/...`
- Added `!lintstatic` to subpackages

## Key Lessons

### Dune's static library resolution

Dune needs two things to link native executables:
1. `.cmxa` files (OCaml native archives) — in `-devel` packages
2. `.a` files (standard archives) — auto-split to `-devel-static` packages

Both `-devel` and `-devel-static` must be in `makedepends` when alt-ergo
links against a library.

### `seq` dependency

The OCaml `seq` library requires a separate dune package
even though the module is in the OCaml stdlib since 4.07.
Dune resolves `seq` through its own package database, which
requires the `seq` opam package to be installed.

### File install vs ocamlfind

For non-dune OCaml packages, installing files to `/usr/lib/ocaml/<pkg>/`
with a `META` file works for dune resolution. Using `ocamlfind install`
is more reliable but requires handling the META file naming (`META` not
`META-zip`) and `-destdir` paths carefully.

## Test

```bash
./cbuild pkg user/alt-ergo
```
