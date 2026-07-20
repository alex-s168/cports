pkgname = "ppx-blob"
pkgver = "0.9.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune", "ppxlib"]
makedepends = [
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppxlib",
    "stdlib-shims",
]
pkgdesc = "OCaml PPX rewriter that includes binary files as strings"
license = "MIT"
url = "https://github.com/johnwhitington/ppx_blob"
source = f"https://github.com/johnwhitington/ppx_blob/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "17a26f1cad8e2497e5fe646e96345ae89f8de732e6ecd1e2e96b2a3f9a426b2d"
# tests require test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "ppx_blob"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ppx_blob",
        "--prefix",
        "/usr",
        "--docdir",
        "/usr/share/doc",
        env={
            **self.make_env,
            "DESTDIR": str(self.chroot_destdir),
        },
    )
    self.install_license("LICENSE.txt")
