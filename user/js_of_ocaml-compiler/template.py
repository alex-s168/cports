pkgname = "js_of_ocaml-compiler"
pkgver = "6.4.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["cmdliner", "dune", "menhir", "ocaml", "ocaml-findlib"]
makedepends = [
    "gen",
    "menhir-lib",
    "menhir-sdk",
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppxlib",
    "sedlex",
    "seq",
    "stdlib-shims",
    "yojson",
]
depends = ["cmdliner", "ocaml-runtime"]
pkgdesc = "Compiler from OCaml bytecode to JavaScript"
license = (
    "GPL-2.0-or-later AND LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception"
)
url = "https://ocsigen.org/js_of_ocaml"
source = (
    f"https://github.com/ocsigen/js_of_ocaml/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "a2151087a8357e96f1d7b58f8acd5005f2ef2b23ef9986834c145188207585c6"
# tests disabled, test infrastructure (ppx_expect, qcheck, re, num) not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "js_of_ocaml-compiler",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
        env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
    )


def post_install(self):
    self.install_license("LICENSE")
