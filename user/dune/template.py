pkgname = "dune"
pkgver = "3.20.2"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib"]
makedepends = ["ocaml-compiler-libs"]
depends = ["ocaml-runtime"]
pkgdesc = "Composable build system for OCaml"
license = "MIT"
url = "https://dune.build"
source = f"https://github.com/ocaml/dune/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "579c738f8ca191ba0a9b22dbe78f1377542442c9827cf4939f8964f09f9edb28"
options = ["!cross"]


def build(self):
    self.do("ocaml", "boot/bootstrap.ml")
    self.do("./_boot/dune.exe", "build", "dune.install", "--release")


def install(self):
    self.do(
        "./_boot/dune.exe",
        "install",
        "dune",
        "--prefix",
        "/usr",
        "--destdir",
        str(self.chroot_destdir),
    )


def post_install(self):
    self.install_license("LICENSE.md")
    # dune installs to /usr/man and /usr/doc instead of /usr/share/man,
    # /usr/share/doc; fix the paths
    man_dir = self.destdir / "usr/man"
    doc_dir = self.destdir / "usr/doc"
    share_man = self.destdir / "usr/share/man"
    share_doc = self.destdir / "usr/share/doc"
    if man_dir.is_dir():
        share_man.parent.mkdir(parents=True, exist_ok=True)
        man_dir.rename(share_man)
    if doc_dir.is_dir():
        share_doc.parent.mkdir(parents=True, exist_ok=True)
        doc_dir.rename(share_doc)
