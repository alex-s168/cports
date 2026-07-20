pkgname = "ppx_blob"
pkgver = "0.9.0"
pkgrel = 0
build_style = "makefile"
make_build_args = []
make_install_args = []
hostmakedepends = ["ocaml", "ocaml-findlib", "ppxlib"]
makedepends = ["ocaml-compiler-libs", "ppxlib"]
depends = ["ocaml-runtime"]
pkgdesc = "OCaml PPX rewriter for including binary blobs as compile-time strings"
license = "Unlicense"
url = "https://github.com/johnwhitington/ppx_blob"
source = f"https://github.com/johnwhitington/ppx_blob/releases/download/{pkgver}/ppx_blob-{pkgver}.tbz"
sha256 = "f115e90a5f1075cedc9d930ab91271f8670ece4dee10dc1147ab39b8afb570e4"
options = ["!cross"]


def build(self):
    self.do("dune", "build", "-p", "ppx_blob", "@install")


def install(self):
    self.do(
        "dune", "install", "-p", "ppx_blob", 
        "--create-install-files", "ppx_blob",
        "--destdir", str(self.chroot_destdir),
        "--libdir", "/usr/lib/ocaml",
        "--bindir", "/usr/bin"
    )


def post_install(self):
    # Remove build artifacts and annotation files
    self.uninstall("usr/lib/ocaml/**/*.cmt", glob=True)
    self.uninstall("usr/lib/ocaml/**/*.cmti", glob=True)