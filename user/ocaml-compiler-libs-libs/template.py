pkgname = "ocaml-compiler-libs"
pkgver = "0.12.4"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml", "ocaml-compiler-libs-system"]
depends = ["ocaml-runtime", "ocaml-compiler-libs-system"]
pkgdesc = "OCaml compiler libraries repackaged"
license = "MIT"
url = "https://github.com/janestreet/ocaml-compiler-libs"
source = (
    f"https://github.com/janestreet/ocaml-compiler-libs/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "f4c37daf975b67c1f645a5d0294ec8ca686b982da410d9f915ccd93548c6e2f1"
options = ["!cross"]


def post_install(self):
    self.install_license("LICENSE.md")
