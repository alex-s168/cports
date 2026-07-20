pkgname = "libantlr3c"
pkgver = "3.4"
pkgrel = 1
build_style = "gnu_configure"
configure_args = ["--disable-antlrdebug", "--enable-64bit"]
# configure script is already shipped in the tarball
configure_gen = []
make_dir = "."
hostmakedepends = ["file", "pkgconf"]
pkgdesc = "ANTLR3 parser generator C runtime library"
license = "BSD-3-Clause"
url = "https://www.antlr3.org"
source = f"{url}/download/C/libantlr3c-{pkgver}.tar.gz"
sha256 = "ca914a97f1a2d2f2c8e1fca12d3df65310ff0286d35c48b7ae5f11dcc8b2eb52"
tool_flags = {"CFLAGS": ["-fexceptions"]}


def post_install(self):
    self.install_license("COPYING")


def pre_configure(self):
    # Avoid unreferenced symbols
    self.rm("src/antlr3debughandlers.c")
    self.do("touch", "src/antlr3debughandlers.c")


@subpackage("libantlr3c-static")
def _(self):
    return ["usr/lib/*.a"]


@subpackage("libantlr3c-devel")
def _(self):
    return self.default_devel()
