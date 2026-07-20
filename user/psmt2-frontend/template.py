pkgname = "psmt2-frontend"
pkgver = "0.4.0"
pkgrel = 1
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune", "menhir"]
makedepends = ["ocaml", "menhir-lib"]
depends = ["ocaml-runtime", "menhir-lib"]
pkgdesc = "SMT-LIB 2 frontend with prenex polymorphism for OCaml"
license = "Apache-2.0"
url = "https://github.com/OCamlPro-Coquera/psmt2-frontend"
source = f"https://github.com/OCamlPro-Coquera/psmt2-frontend/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "06eff884b629ce30704d08fb4559e54812e8c234e6086da770ea693613fe9780"
options = ["!cross", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "psmt2-frontend",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
        env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
    )

    self.install_license("LICENSE")
