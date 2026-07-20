pkgname = "kissat"
pkgver = "4.0.4"
pkgrel = 0
build_style = "configure"
make_check_target = "test"
pkgdesc = "SAT solver"
license = "MIT"
url = "https://fmv.jku.at/kissat"
source = f"https://github.com/arminbiere/kissat/archive/refs/tags/rel-{pkgver}.tar.gz"
sha256 = "bfe93eaa6323b48011e4b1fcf74b3f2e20f9de544767e728009e5b2018296193"
# cross: ./configure attempts to run built executables during configuration
options = ["!cross"]


def install(self):
    self.install_bin("build/kissat")
    self.install_lib("build/libkissat.a")
    self.install_file("src/kissat.h", "usr/include")
    self.install_license("LICENSE")


@subpackage("kissat-devel")
def _(self):
    return self.default_devel()
