pkgname = "seq"
pkgver = "0.3.1"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
pkgdesc = "Compatibility package for OCaml's standard iterator type"
license = "LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception"
url = "https://github.com/c-cube/seq"
source = f"https://github.com/c-cube/seq/archive/v{pkgver}.tar.gz"
sha256 = "6bc8beb15f0a678dbd6f8b4f75a2cc45fa2d9e4cf545eafe9fb057c97c9914cf"
options = ["!cross", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "seq",
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
