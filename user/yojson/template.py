pkgname = "yojson"
pkgver = "3.0.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Optimized parsing and printing library for the JSON format"
license = "BSD-3-Clause"
url = "https://github.com/ocaml-community/yojson"
source = f"https://github.com/ocaml-community/yojson/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "03676bd68a7ccc9e4aeb954930a401cf9389ba86e6cf4a61ad768cb3fac23856"
# tests require alcotest which is not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "yojson",
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
