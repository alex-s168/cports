pkgname = "cmdliner"
pkgver = "2.1.1"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
pkgdesc = "Declarative definition of command line interfaces for OCaml"
license = "ISC"
url = "https://erratique.ch/software/cmdliner"
source = (
    f"https://github.com/dbuenzli/cmdliner/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "90dee3ef327fb7db1eb5859be7143ea9b60e37534865a725e2fcb92569a38370"
options = ["!cross", "!lintstatic", "!lintcomp"]


def build(self):
    self.do("make", "all")


def install(self):
    self.do(
        "make",
        "install",
        "PREFIX=/usr",
        env={"DESTDIR": str(self.chroot_destdir)},
    )


def post_install(self):
    self.install_license("LICENSE.md")
