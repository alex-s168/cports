pkgname = "sexplib0"
pkgver = "0.17.0"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml"]
pkgdesc = "Library for S-expression serialization"
license = "MIT"
url = "https://github.com/janestreet/sexplib0"
source = (
    f"https://github.com/janestreet/sexplib0/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "5b0910b5dab8ec63633be5dbf92a3e4863d415d803cad9dddf99dba43ce7498b"
options = ["!cross", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "sexplib0",
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
