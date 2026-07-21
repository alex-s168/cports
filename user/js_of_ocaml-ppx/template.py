pkgname = "js_of_ocaml-ppx"
pkgver = "6.4.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib", "ppxlib"]
makedepends = [
    "js_of_ocaml",
    "ocaml",
    "ocaml-compiler-libs",
    "ocaml-compiler-libs-janestreet",
    "ppxlib",
    "stdlib-shims",
]
depends = ["js_of_ocaml", "ocaml-runtime"]
pkgdesc = "PPX syntax extension for js_of_ocaml"
license = (
    "GPL-2.0-or-later AND LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception"
)
url = "https://ocsigen.org/js_of_ocaml"
source = (
    f"https://github.com/ocsigen/js_of_ocaml/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "a2151087a8357e96f1d7b58f8acd5005f2ef2b23ef9986834c145188207585c6"
# tests disabled, test infrastructure (ppx_expect, re, num) not packaged
options = ["!cross", "!check", "!lintstatic"]


def post_extract(self):
    # Replace the jbuild-plugin-based version tool (uses Toploop.directive_table
    # from OCaml's toplevel library, not available in distro packages)
    (self.cwd / "tools/version/dune").write_text(
        "(rule\n"
        "  (target GIT-VERSION)\n"
        '  (action (with-stdout-to %{target} (echo ""))))\n'
    )


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "js_of_ocaml-ppx",
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
