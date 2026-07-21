pkgname = "ocaml-re"
pkgver = "1.14.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Pure OCaml regular expression library"
license = "LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception"
url = "https://github.com/ocaml/ocaml-re"
source = f"https://github.com/ocaml/ocaml-re/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "e32eb4c6f319ff74241da9e1b00032f990241347271baf3adb468faaaa616147"
# tests require ppx_expect, ounit2, js_of_ocaml which are not packaged
options = ["!cross", "!check", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "re"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "re",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
        env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
    )


def post_install(self):
    self.install_license("LICENSE.md")
