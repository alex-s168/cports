pkgname = "symfpu"
pkgver = "0.0.0"
pkgrel = 0
pkgdesc = "Symbolic floating point unit - header-only library for cvc5"
license = "BSD-3-Clause"
url = "https://github.com/cvc5/symfpu"
source = [
    "https://github.com/cvc5/symfpu/archive/227a7246b8ce513b393cc2645d6d65d3490ea1de.tar.gz",
]
sha256 = [
    "ff22e37dbc133120ada5760878974811737bec65b12a8883f92b1ed9e3f96e99",
]


def install(self):
    self.install_dir("usr/include/symfpu")
    self.install_files("core", "usr/include/symfpu")
    self.install_files("utils", "usr/include/symfpu")
    self.install_license("LICENSE")
