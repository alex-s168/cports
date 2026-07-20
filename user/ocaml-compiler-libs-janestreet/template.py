pkgname = "ocaml-compiler-libs-janestreet"
pkgver = "0.17.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml", "ocaml-compiler-libs"]
depends = ["ocaml-runtime", "ocaml-compiler-libs"]
pkgdesc = "OCaml compiler libraries repackaged"
license = "MIT"
url = "https://github.com/janestreet/ocaml-compiler-libs"
source = f"https://github.com/janestreet/ocaml-compiler-libs/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "9b9644d7351db699e57ddba7c767bb4153e6e988ccf45ead2fb238a3bd75cdc7"
options = ["!cross", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "ocaml-compiler-libs"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ocaml-compiler-libs",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
        env={
            **self.make_env,
            "DESTDIR": str(self.chroot_destdir),
        },
    )


def post_install(self):
    self.install_license("LICENSE.md")
