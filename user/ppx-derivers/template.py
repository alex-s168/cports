pkgname = "ppx-derivers"
pkgver = "1.2.1"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml"]
pkgdesc = "Shared PPX derivers for OCaml"
license = "BSD-2-Clause"
url = "https://github.com/ocaml-ppx/ppx_derivers"
source = f"https://github.com/ocaml-ppx/ppx_derivers/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "b6595ee187dea792b31fc54a0e1524ab1e48bc6068d3066c45215a138cc73b95"
options = ["!cross", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "ppx_derivers"


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "ppx_derivers",
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
