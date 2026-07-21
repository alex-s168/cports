pkgname = "ocamlgraph"
pkgver = "2.2.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Generic graph library for OCaml"
license = "LGPL-2.1-only"
url = "https://github.com/backtracking/ocamlgraph"
source = f"https://github.com/backtracking/ocamlgraph/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "0c183118bc62fb0851fac5e195293067cf8863edd2dabf322d20583d65bb7758"
# tests disabled, test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ocamlgraph",
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
