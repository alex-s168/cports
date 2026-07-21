pkgname = "sedlex"
pkgver = "3.7"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib", "ppxlib"]
makedepends = [
    "gen",
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppxlib",
    "seq",
    "stdlib-shims",
]
depends = ["ocaml-compiler-libs", "ocaml-runtime"]
pkgdesc = "Unicode lexer generator for OCaml"
license = "MIT"
url = "https://github.com/ocaml-community/sedlex"
source = f"https://github.com/ocaml-community/sedlex/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "edb489710f5f937e69c7c11bb165fca91595d35059990c877c79f292b3e00851"
# tests require ppx_expect which is not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "sedlex",
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
