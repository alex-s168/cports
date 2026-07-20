pkgname = "ppx-deriving"
pkgver = "6.1.1"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune", "cppo"]
makedepends = [
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppx-derivers",
    "ppxlib",
    "stdlib-shims",
]
depends = ["ocaml-runtime", "ppxlib", "ppx-derivers"]
pkgdesc = "Type-driven code generation for OCaml"
license = "MIT"
url = "https://github.com/ocaml-ppx/ppx_deriving"
source = f"https://github.com/ocaml-ppx/ppx_deriving/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "6fab6e1e894207db268f2103beba5ec9cdc10c066f6ed4f12e748ce97b027757"
# tests require test infrastructure not packaged
options = ["!cross", "!check", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "ppx_deriving"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ppx_deriving",
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
