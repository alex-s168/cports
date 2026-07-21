pkgname = "mlmpfr"
pkgver = "4.2.1"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["dune-configurator", "mpfr-devel", "ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "OCaml bindings for the MPFR library"
license = "LGPL-3.0-only"
url = "https://github.com/thvnx/mlmpfr"
source = (
    f"https://github.com/thvnx/mlmpfr/archive/refs/tags/mlmpfr.{pkgver}.tar.gz"
)
sha256 = "8e36013b257e946542810bd66fad815b2c941903ceaafdea9a060b388bd38797"
# tests disabled, test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "mlmpfr",
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
