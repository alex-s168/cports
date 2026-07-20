pkgname = "camlzip"
pkgver = "1.11"
pkgrel = 2
build_style = "makefile"
hostmakedepends = ["ocaml", "ocaml-findlib"]
makedepends = ["ocaml", "zlib-ng-compat-devel"]
depends = ["ocaml-runtime"]
pkgdesc = "OCaml library for reading and writing compressed files"
license = "LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception"
url = "https://github.com/xavierleroy/camlzip"
source = f"https://github.com/xavierleroy/camlzip/archive/refs/tags/rel{''.join(pkgver.split('.'))}.tar.gz"
sha256 = "ffbbc5de3e1c13dc0e59272376d232d2ede91b327551063d47fddb74f1d5ed37"
# no check target in Makefile
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    # Install zip package to findlib-understandable location
    zipdir = "usr/lib/ocaml/zip"
    self.install_dir(zipdir)
    seen = set()
    for pat in [
        "*.cma",
        "*.cmxa",
        "*.cmxs",
        "*.cmi",
        "*.cmt",
        "*.cmti",
        "*.cmx",
        "*.a",
        "*.so",
        "*.ml",
        "*.mli",
    ]:
        for f in self.cwd.glob(pat):
            fn = f.name
            if fn not in seen:
                seen.add(fn)
                self.install_file(fn, zipdir)
    # Install META (renamed from META-zip)
    self.install_file("META-zip", zipdir, name="META")

    # Install camlzip virtual package
    camlzipdir = "usr/lib/ocaml/camlzip"
    self.install_dir(camlzipdir)
    self.install_file("META-camlzip", camlzipdir, name="META")

    self.install_license("LICENSE")
