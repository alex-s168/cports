pkgname = "pp-loc"
pkgver = "2.1.0"
pkgrel = 1
build_style = "dune"
make_env = {"DUNE_BUILD_SERVER": "0"}
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
pkgdesc = "Quote and highlight input fragments at a given source location"
license = "MIT"
url = "https://github.com/Armael/pp_loc"
source = f"https://github.com/Armael/pp_loc/releases/download/v{pkgver}/pp_loc-{pkgver}.tbz"
sha256 = "2f736505d431e81a4fe851ad310ff29ec4cd20c8fd37ef050d9e6f1050baa7cb"
# tests require test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "pp_loc"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "pp_loc",
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
