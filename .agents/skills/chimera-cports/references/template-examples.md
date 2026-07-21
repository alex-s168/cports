# Template examples

Use these as shapes, not copy-paste substitutes. Verify every field and dependency against the released source and nearby current templates.

## Happy path: system-library Meson package

```python
pkgname = "libsample"
pkgver = "1.2.3"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf"]
makedepends = ["libother-devel"]
pkgdesc = "Small sample processing library"
license = "MIT"
url = "https://example.org/libsample"
source = f"https://example.org/releases/libsample-{pkgver}.tar.xz"
sha256 = "<verified-sha256>"


def post_install(self):
    self.install_license("LICENSE")


@subpackage("libsample-devel")
def _(self):
    return self.default_devel()
```

Why this is preferred:

- build tooling and target dependencies are classified separately
- the build style supplies standard configure/build/check/install behavior
- shared-library runtime dependencies are scanner-generated
- development files are split with the standard helper

Create the subpackage symlink with:

```sh
./cbuild relink-subpkgs user/libsample
```

## Robust variant: missing reusable dependency

If `sample-app` needs `libcodec` and no cports package provides it, create two templates:

```text
user/libcodec/template.py
user/sample-app/template.py
```

Package `libcodec` from its stable upstream release with its own metadata, tests, license, and `libcodec-devel` subpackage. Then declare only the build interface in the application:

```python
pkgname = "sample-app"
pkgver = "2.0.0"
pkgrel = 0
build_style = "cmake"
hostmakedepends = ["cmake", "ninja", "pkgconf"]
makedepends = ["libcodec-devel"]
pkgdesc = "Application for processing sample data"
license = "BSD-2-Clause"
url = "https://example.org/sample-app"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "<verified-sha256>"
```

Build `user/libcodec` first for focused diagnosis, then run the required final command:

```sh
./cbuild pkg user/sample-app
```

Cbuild can recursively build the missing dependency. Keeping the packages separate permits independent updates, security fixes, reuse, and dependency scanning.

## Anti-pattern and correction

Bad:

```python
# Do not do this merely because libcodec is absent from cports.
source = [
    f"https://example.org/sample-app-{pkgver}.tar.gz",
    "https://example.org/libcodec-0.9.tar.gz",
]
options = ["!check", "!cross"]


def pre_configure(self):
    self.do("sed", "-i", "s/-O3/-O2/", "Makefile")
```

Problems:

- bundles a reusable dependency without proving an outdated/modified-version requirement
- disables tests and cross compilation to avoid solving failures
- mutates source ad hoc
- replaces upstream or cbuild compiler policy

Correct:

1. Package the current compatible `libcodec` release separately.
2. Add `libcodec-devel` to `makedepends`.
3. Keep checks and cross compilation enabled.
4. If source changes are genuinely required, add a focused patch under `patches/`, explain its purpose in the patch, and prefer an upstreamable fix.
5. If upstream demonstrably requires a patched or obsolete embedded `libcodec`, retain only that dependency, add a concise evidence-based template comment, and continue separating all other dependencies.
