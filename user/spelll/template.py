pkgname = "spelll"
pkgver = "0.4"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml", "seq", "stdlib-shims"]
pkgdesc = "Fuzzy string searching using Levenshtein automaton for OCaml"
license = "BSD-2-Clause"
url = "https://github.com/c-cube/spelll"
source = f"https://github.com/c-cube/spelll/archive/v{pkgver}.tar.gz"
sha256 = "b8505685172b90b2ddd013b22223c410a3c234050db002000fdad08aaa435b1b"
# tests require qcheck which is not packaged
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "spelll",
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
