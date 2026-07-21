pkgname = "camlidl"
pkgver = "1.13"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Stub code generator for OCaml"
license = "LGPL-2.0-or-later WITH OCaml-LGPL-linking-exception"
url = "https://github.com/xavierleroy/camlidl"
# tag is camlidl113, not camlidl1.13
source = (
    "https://github.com/xavierleroy/camlidl/archive/refs/tags/camlidl113.tar.gz"
)
sha256 = "c82bfd106208ebedd8c264300e939010f87eed83e6f6339e3a6cf8f66caeed54"
options = ["!cross", "!lintstatic"]


def configure(self):
    self.cp("config/Makefile.unix", "config/Makefile")
    # Fix BINDIR from /usr/local/bin to /usr/bin
    with (self.cwd / "config" / "Makefile").open("r") as f:
        content = f.read()
    content = content.replace("/usr/local/bin", "/usr/bin")
    with (self.cwd / "config" / "Makefile").open("w") as f:
        f.write(content)
    # Add mkdir -p to compiler install (no DESTDIR support in original)
    with (self.cwd / "compiler" / "Makefile").open("r") as f:
        content = f.read()
    content = content.replace(
        "\tcp $(PROG) $(BINDIR)",
        "\tmkdir -p $(DESTDIR)$(BINDIR)\n\tcp $(PROG) $(DESTDIR)$(BINDIR)",
    )
    with (self.cwd / "compiler" / "Makefile").open("w") as f:
        f.write(content)
    # Add mkdir -p to runtime install
    with (self.cwd / "runtime" / "Makefile.unix").open("r") as f:
        content = f.read()
    content = content.replace(
        "\tcp camlidlruntime.h",
        "\tmkdir -p $(DESTDIR)$(OCAMLLIB)/caml\n\tcp camlidlruntime.h",
    )
    content = content.replace(
        "\tcp dllcamlidl.so",
        "\tmkdir -p $(DESTDIR)$(OCAMLLIB)/stublibs\n\tcp dllcamlidl.so",
    )
    with (self.cwd / "runtime" / "Makefile.unix").open("w") as f:
        f.write(content)


def build(self):
    self.do("make", "all")


def install(self):
    destdir = str(self.chroot_destdir)
    self.do("make", "install", f"DESTDIR={destdir}")
    self.install_file("META", "usr/lib/ocaml/camlidl")


def post_install(self):
    self.install_license("LICENSE")
