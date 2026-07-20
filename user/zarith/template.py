pkgname = "zarith"
pkgver = "1.14"
pkgrel = 1
hostmakedepends = ["ocaml", "ocaml-findlib", "pkgconf"]
makedepends = ["ocaml-compiler-libs", "gmp-devel"]
depends = ["ocaml-runtime"]
pkgdesc = "Arbitrary-precision integer arithmetic for OCaml"
license = "LGPL-2.0-only WITH OCaml-LGPL-linking-exception"
url = "https://github.com/ocaml/Zarith"
source = (
    f"https://github.com/ocaml/Zarith/archive/refs/tags/release-{pkgver}.tar.gz"
)
sha256 = "5db9dcbd939153942a08581fabd846d0f3f2b8c67fe68b855127e0472d4d1859"
hardening = ["!int"]
options = ["!cross", "!lintstatic"]


def configure(self):
    self.do("./configure", "-installdir", "/usr/lib/ocaml")


def build(self):
    self.do("make")


def check(self):
    self.do("make", "tests")


def install(self):
    instdir = str(self.chroot_destdir / "usr/lib/ocaml")
    self.do("make", "install", f"INSTALLDIR={instdir}", "INSTMETH=install")
    # Install META file for ocamlfind/dune
    self.install_file("META", "usr/lib/ocaml/zarith")


def post_install(self):
    self.install_license("LICENSE")
