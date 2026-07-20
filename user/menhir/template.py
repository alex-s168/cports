pkgname = "menhir"
pkgver = "20250912"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml-compiler-libs"]
depends = ["ocaml-runtime"]
pkgdesc = "LR(1) parser generator for OCaml"
license = "LGPL-2.0-only"
url = "http://gallium.inria.fr/~fpottier/menhir"
source = f"https://gitlab.inria.fr/fpottier/menhir/-/archive/{pkgver}/menhir-{pkgver}.tar.gz"
sha256 = "26b1f44d6b4ed634631c50866e5535062591308a01a987f415411a9543965c9b"
options = ["!cross", "!lintstatic"]


def init_configure(self):
    self.dune._override_pkgname = "menhir,menhirLib,menhirSdk,menhirCST"


def install(self):
    for pkg in ["menhir", "menhirLib", "menhirSdk", "menhirCST"]:
        self.do(
            "dune",
            "install",
            "-p",
            pkg,
            "--prefix",
            "/usr",
            "--libdir",
            "/usr/lib",
            "--mandir",
            "/usr/share/man",
            "--docdir",
            "/usr/share/doc",
            env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
        )


def post_install(self):
    self.install_license("LICENSE")


@subpackage("menhir-lib")
def _(self):
    self.subdesc = "runtime library"
    self.depends = [self.parent]
    self.options = ["!lintstatic"]
    return ["usr/lib/menhirLib"]


@subpackage("menhir-sdk")
def _(self):
    self.subdesc = "development SDK"
    self.depends = [self.with_pkgver("menhir")]
    self.options = ["!lintstatic"]
    return ["usr/lib/menhirSdk"]


@subpackage("menhir-cst")
def _(self):
    self.subdesc = "concrete syntax tree library"
    self.depends = [self.with_pkgver("menhir")]
    self.options = ["!lintstatic"]
    return ["usr/lib/menhirCST"]
