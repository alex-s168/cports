pkgname = "dune-configurator"
pkgver = "3.20.2"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["ocaml", "ocaml-findlib", "dune"]
makedepends = ["ocaml", "dune", "csexp"]
depends = ["ocaml-runtime", "dune", "csexp"]
pkgdesc = "Helper library for gathering system configuration"
license = "MIT"
url = "https://github.com/ocaml/dune"
source = f"https://github.com/ocaml/dune/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "579c738f8ca191ba0a9b22dbe78f1377542442c9827cf4939f8964f09f9edb28"
# tests disabled, test infrastructure not packaged
options = ["!cross", "!lintstatic", "!check"]


def init_configure(self):
    self.dune._override_pkgname = "dune-configurator"
    # Remove vendored copies to force use of system packages
    self.rm("vendor/csexp", recursive=True)
    self.rm("vendor/pp", recursive=True)


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "dune-configurator",
        "--prefix",
        "/usr",
        "--docdir",
        "/usr/share/doc",
        env={
            **self.make_env,
            "DESTDIR": str(self.chroot_destdir),
        },
    )
    self.install_license("LICENSE.md")
