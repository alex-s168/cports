pkgname = "csexp"
pkgver = "1.5.2"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Parsing and printing of S-expressions in Canonical form"
license = "MIT"
url = "https://github.com/ocaml-dune/csexp"
source = (
    f"https://github.com/ocaml-dune/csexp/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "de3fda861ec8210a404fcb76afa162b08ed1cd11228645c78b53e1f82b24e236"
# tests disabled, test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "csexp",
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
