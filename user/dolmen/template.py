pkgname = "dolmen"
pkgver = "0.10"
pkgrel = 1
build_style = "dune"
make_env = {"DUNE_BUILD_SERVER": "0"}
hostmakedepends = ["ocaml", "ocaml-findlib", "dune", "menhir"]
makedepends = [
    "fmt-ocaml-devel",
    "gen",
    "hmap",
    "menhir-lib",
    "ocaml",
    "pp-loc",
    "seq",
    "spelll",
    "stdlib-shims",
    "uutf",
    "zarith",
]
depends = ["ocaml-runtime"]
pkgdesc = "OCaml library for SMT-LIB and TPTP parsing"
license = "BSD-2-Clause"
url = "https://github.com/Gbury/dolmen"
source = f"https://github.com/Gbury/dolmen/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "d5df9e7610276e55c136de80d518c5e73fed4cd623ed24237544fdc8cc9e9126"
# tests require qcheck which is not packaged
options = ["!cross", "!check", "!lintstatic"]


def init_configure(self):
    # Build all sub-packages in one go
    self.dune._override_pkgname = "dolmen,dolmen_type,dolmen_loop"


def install(self):
    # Install without --create-install-files to avoid overwriting
    # the .install file generated during build (which lists all sub-libs).
    dune_args = [
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
    ]
    for pkg in ["dolmen", "dolmen_type", "dolmen_loop"]:
        self.do(
            "dune",
            "install",
            "-p",
            pkg,
            *dune_args,
            env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
        )


def post_install(self):
    self.install_license("LICENSE")


@subpackage("dolmen-type")
def _(self):
    self.subdesc = "typechecking library"
    self.options = ["!lintstatic"]
    self.depends = [
        self.with_pkgver("dolmen"),
        "spelll",
        "uutf",
    ]

    return ["usr/lib/dolmen_type"]


@subpackage("dolmen-loop")
def _(self):
    self.subdesc = "tool library for automated deduction"
    self.options = ["!lintstatic"]
    self.depends = [
        self.with_pkgver("dolmen"),
        self.with_pkgver("dolmen-type"),
        "gen",
        "pp-loc",
    ]

    return ["usr/lib/dolmen_loop"]
