pkgname = "why3"
pkgver = "1.8.2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--disable-frama-c",
    "--disable-coq-libs",
    "--disable-pvs-libs",
    "--disable-isabelle-libs",
    "--disable-ide",
    "--disable-web-ide",
    "--disable-mpfr",
    "--disable-hypothesis-selection",
    "--disable-stackify",
    "--disable-re",
    "--disable-sexp",
]
configure_gen = []
make_dir = "."
# menhirLib is at /usr/lib/menhirLib/ but ocamlfind searches in
# /usr/lib/ocaml/. Tell ocamlfind where to find it.
env = {"OCAMLPATH": "/usr/lib"}

hostmakedepends = [
    "menhir",
    "ocaml",
    "ocaml-findlib",
    "pkgconf",
]
makedepends = [
    "camlzip",
    "gmp-devel",
    "menhir-lib",
    "ocaml-compiler-libs",
    "zarith",
    "zlib-ng-compat-devel",
]
depends = ["ocaml-runtime"]
pkgdesc = "Platform for deductive program verification"
license = "LGPL-2.1-only"
url = "https://www.why3.org"
source = f"https://why3.gitlabpages.inria.fr/releases/why3-{pkgver}.tar.gz"
sha256 = "b7d112edd5bcce6bcce0023d2bc834eb2ae1a1c42d7aea44ffa124d649b50bea"
# tests require external provers to be installed
options = ["!check", "!lintstatic"]


def build(self):
    self.make.build()


def check(self):
    self.make.check()


def install(self):
    destdir = str(self.chroot_destdir)
    self.make.install()
    # Build and install the OCaml library
    self.do("make", "byte")
    self.do("make", "install-lib", "DESTDIR=" + destdir)


def post_install(self):
    self.install_license("LICENSE")

    # Remove .cmt/.cmti files from the main package - they're development
    # files that should go in -devel
    for d in ["ocaml/why3", "why3"]:
        libd = self.destdir / "usr/lib" / d
        if libd.is_dir():
            for f in libd.rglob("*.cmt"):
                f.unlink()
            for f in libd.rglob("*.cmti"):
                f.unlink()


@subpackage("why3-libs")
def _(self):
    self.subdesc = "libraries"
    self.depends = [self.with_pkgver("why3")]
    self.options = ["!lintstatic"]
    # .cma (bytecode) and .cmxs (native shared) are runtime-loadable
    return [
        "usr/lib/ocaml/why3/*.cma",
        "usr/lib/ocaml/why3/*.cmxs",
        "usr/lib/ocaml/why3/META",
    ]


@subpackage("why3-devel")
def _(self):
    self.subdesc = "development files"
    self.depends = [self.with_pkgver("why3-libs")]
    self.options = ["!lintstatic"]
    return [
        "usr/lib/ocaml/why3/*.a",
        "usr/lib/ocaml/why3/*.cmi",
        "usr/lib/ocaml/why3/*.cmx",
        "usr/lib/ocaml/why3/*.cmxa",
    ]
