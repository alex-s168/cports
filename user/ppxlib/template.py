pkgname = "ppxlib"
pkgver = "0.37.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune", "cppo"]
makedepends = [
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppx-derivers",
    "sexplib0",
    "stdlib-shims",
]
depends = ["ocaml-runtime", "sexplib0", "ppx-derivers"]
pkgdesc = "Standard library for OCaml PPX rewriters"
license = "MIT"
url = "https://github.com/ocaml-ppx/ppxlib"
source = (
    f"https://github.com/ocaml-ppx/ppxlib/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "e41d37507ce6f8ea47d6d41e62e0881139bd1f0c9d2ff982d9cd3048756aafbf"
# Tests disabled as test infrastructure has complex transitive deps
options = ["!cross", "!lintstatic", "!check"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ppxlib",
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
