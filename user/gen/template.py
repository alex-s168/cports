pkgname = "gen"
pkgver = "1.1"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml", "seq"]
pkgdesc = "Simple, efficient iterators for OCaml"
license = "BSD-2-Clause"
url = "https://github.com/c-cube/gen"
source = f"https://github.com/c-cube/gen/archive/v{pkgver}.tar.gz"
sha256 = "6893bf156bbaa4254ec5ec2ea5fe539030f2395bc5cd83ccb8fe3930cff89cb0"
# tests require qcheck and ounit which are not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "gen",
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
