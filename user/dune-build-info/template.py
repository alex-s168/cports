pkgname = "dune-build-info"
pkgver = "3.20.2"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml", "dune"]
depends = ["ocaml-runtime", "dune"]
pkgdesc = "Embed build information inside executable"
license = "MIT"
url = "https://github.com/ocaml/dune"
source = f"https://github.com/ocaml/dune/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "579c738f8ca191ba0a9b22dbe78f1377542442c9827cf4939f8964f09f9edb28"
# tests disabled, test infrastructure not packaged
options = ["!cross", "!lintstatic", "!check"]


def init_configure(self):
    self.dune._override_pkgname = "dune-build-info"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "dune-build-info",
        "--prefix",
        "/usr",
        "--docdir",
        "/usr/share/doc",
        env={
            **self.make_env,
            "DESTDIR": str(self.chroot_destdir),
        },
    )
    self.install_license("LICENSE.md")
