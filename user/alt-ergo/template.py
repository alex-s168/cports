pkgname = "alt-ergo"
pkgver = "2.6.3"
pkgrel = 0
build_style = "dune"
hostmakedepends = [
    "cppo",
    "dune",
    "menhir",
    "ocaml",
    "ocaml-findlib",
    "ppxlib",
]
makedepends = [
    "camlzip",
    "cmdliner",
    "dolmen",
    "dolmen-loop",
    "dolmen-type",
    "dune-build-info",
    "dune-private-libs",
    "dune-site",
    "fmt-ocaml-devel",
    "fmt-ocaml-devel-static",
    "gmp-devel",
    "gmp-devel-static",
    "hmap",
    "logs-ocaml",
    "logs-ocaml-devel",
    "logs-ocaml-devel-static",
    "menhir-lib",
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ocplib-simplex",
    "ppx-blob",
    "ppx-derivers",
    "ppx-deriving",
    "psmt2-frontend",
    "seq",
    "sexplib0",
    "stdlib-shims",
    "zarith",
    "zlib-ng-compat-devel",
]


# Build alt-ergo, alt-ergo-lib, and alt-ergo-parsers together
# as they're all part of the same dune project
def init_configure(self):
    self.dune._override_pkgname = "alt-ergo,alt-ergo-lib,alt-ergo-parsers"


def install(self):
    for pkg in ["alt-ergo", "alt-ergo-lib", "alt-ergo-parsers"]:
        self.do(
            "dune",
            "install",
            "-p",
            pkg,
            "--prefix",
            "/usr",
            "--libdir",
            "/usr/lib",
            "--docdir",
            "/usr/share/doc",
            "--mandir",
            "/usr/share/man",
            env={
                **self.make_env,
                "DESTDIR": str(self.chroot_destdir),
            },
        )


depends = ["ocaml-runtime"]
pkgdesc = "Alt-Ergo SMT prover"
license = "custom:ocamlpro-non-commercial OR Apache-2.0"
url = "https://alt-ergo.ocamlpro.com"
source = f"https://github.com/OCamlPro/alt-ergo/releases/download/v{pkgver}/alt-ergo-{pkgver}.tbz"
sha256 = "4ac2b5d8ae6c54a11a0cc349ec76a153aa95727bf57ef9cb3309a706a7fb1bfa"
# tests require qcheck which is not packaged
options = ["!cross", "!check", "!lintstatic"]


def post_install(self):
    self.install_license("LICENSE.md")


@subpackage("alt-ergo-lib")
def _(self):
    self.subdesc = "core library"
    self.options = ["!lintstatic"]
    self.depends = [
        self.with_pkgver("alt-ergo"),
    ]

    return ["usr/lib/alt-ergo-lib"]


@subpackage("alt-ergo-parsers")
def _(self):
    self.subdesc = "parser library"
    self.options = ["!lintstatic"]
    self.depends = [
        self.with_pkgver("alt-ergo"),
    ]

    return ["usr/lib/alt-ergo-parsers"]
