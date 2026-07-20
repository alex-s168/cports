pkgname = "cppo"
pkgver = "1.7.0"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "C-style preprocessor for OCaml"
license = "BSD-3-Clause"
url = "https://github.com/ocaml-community/cppo"
source = f"https://github.com/ocaml-community/cppo/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "7df72f6f240ec6d4d5bc6bcb2e8cfc825ade11594dc93243f1b821b5766548e1"
options = ["!cross", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "cppo",
        "--prefix",
        "/usr",
        "--docdir",
        "/usr/share/doc",
        env={
            **self.make_env,
            "DESTDIR": str(self.chroot_destdir),
        },
    )


def post_install(self):
    self.install_license("LICENSE.md")
