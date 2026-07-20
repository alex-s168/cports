pkgname = "ocplib-simplex"
pkgver = "0.5.1"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = [
    "logs-ocaml",
    "logs-ocaml-devel",
    "ocaml",
]
pkgdesc = "Simplex algorithm implementation for OCaml"
license = "LGPL-2.1-only"
url = "https://github.com/OCamlPro/ocplib-simplex"
source = f"https://github.com/OCamlPro/ocplib-simplex/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "4518a8c9eaaaee4626f73899a2b87a482f55c3a6995303f08eea8c952c7befa5"
# Tests require zarith, gmp-devel, and logs-ocaml-devel-static for native linking
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ocplib-simplex",
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
