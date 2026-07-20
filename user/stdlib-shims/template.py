pkgname = "stdlib-shims"
pkgver = "0.3.0"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml", "ocaml-compiler-libs"]
pkgdesc = "Backport some of the new stdlib features to older compiler"
license = "LGPL-2.1-only WITH OCaml-LGPL-linking-exception"
url = "https://github.com/ocaml/stdlib-shims"
source = (
    f"https://github.com/ocaml/stdlib-shims/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "6d0386313a021146300011549180fcd4e94f7ac3c3bf021ff165f6558608f0c2"
options = ["!cross", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "stdlib-shims",
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
    self.install_license("LICENSE")
