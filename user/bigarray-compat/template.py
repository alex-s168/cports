pkgname = "bigarray-compat"
pkgver = "1.1.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Compatibility library to use Stdlib.Bigarray when possible"
license = "ISC"
url = "https://github.com/mirage/bigarray-compat"
source = f"https://github.com/mirage/bigarray-compat/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "cf09354986d1ab7d506949f58e73dd72be8aedb241c1593381c18e92a70c0bb1"
options = ["!cross", "!lintstatic"]


def init_configure(self):
    # Replace the ancient jbuilder-style dune file with a modern static one.
    self.rm("dune-project")
    self.rm("src/dune")
    with (self.cwd / "dune-project").open("w") as f:
        f.write("(lang dune 2.7)\n")
        f.write("(name bigarray-compat)\n")
    with (self.cwd / "src" / "dune").open("w") as f:
        f.write("(library\n")
        f.write(" (name bigarray_compat)\n")
        f.write(" (public_name bigarray-compat)\n")
        f.write(" (modules bigarray_compat)\n")
        f.write(" (wrapped false))\n")
        f.write("(rule\n")
        f.write(" (targets bigarray_compat.ml)\n")
        f.write(" (action (copy bigarray_stdlib.ml bigarray_compat.ml)))\n")


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "bigarray-compat",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib/ocaml",
        "--docdir",
        "/usr/share/doc",
        env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
    )


def post_install(self):
    self.install_license("LICENSE.md")
