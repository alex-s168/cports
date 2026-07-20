pkgname = "ocamlbuild"
pkgver = "0.15.0"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib"]
makedepends = ["ocaml-compiler-libs"]
depends = ["ocaml-runtime"]
pkgdesc = "Generic build tool for OCaml"
license = "LGPL-2.1-only WITH OCaml-LGPL-linking-exception"
url = "https://github.com/ocaml/ocamlbuild"
source = (
    f"https://github.com/ocaml/ocamlbuild/archive/refs/tags/{pkgver}.tar.gz"
)
sha256 = "d3f6ee73100b575d4810247d10ed8f53fccef4e90daf0e4a4c5f3e6a3030a9c9"
options = ["!cross", "!lintstatic"]


def build(self):
    ocamlbuild_prefix = "/usr"
    self.do(
        "make",
        "-f",
        "configure.make",
        "all",
        f"OCAMLBUILD_PREFIX={ocamlbuild_prefix}",
    )
    self.do(
        "make",
        "check-if-preinstalled",
        "all",
        f"OCAMLBUILD_PREFIX={ocamlbuild_prefix}",
    )


def install(self):
    self.install_bin("ocamlbuild.native", name="ocamlbuild")
    self.install_bin("ocamlbuild.byte")
    ocaml_dest = "usr/lib/ocaml"
    self.install_dir(f"{ocaml_dest}/ocamlbuild")
    for f in [
        "ocamlbuild.cmo",
        "ocamlbuild.cmx",
        "ocamlbuild.cmi",
        "ocamlbuild.cma",
        "ocamlbuild.cmxa",
        "ocamlbuild.a",
    ]:
        p = self.cwd / f
        if p.exists():
            self.install_file(str(p), f"{ocaml_dest}/ocamlbuild")
    # also install plugin lib and signatures
    for d in ["src", "plugin-lib"]:
        for f in (self.cwd / d).glob("*.cmi"):
            self.install_file(str(f), f"{ocaml_dest}/ocamlbuild")
    self.install_file(
        "plugin-lib/ocamlbuildlib.cma", f"{ocaml_dest}/ocamlbuild"
    )
    self.install_file(
        "plugin-lib/ocamlbuildlib.cmxa", f"{ocaml_dest}/ocamlbuild"
    )
    self.install_file("plugin-lib/ocamlbuildlib.a", f"{ocaml_dest}/ocamlbuild")


def post_install(self):
    self.install_license("LICENSE")
