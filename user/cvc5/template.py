pkgname = "cvc5"
pkgver = "1.3.4"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DCMAKE_BUILD_TYPE=Production",
    "-DBUILD_SHARED_LIBS=ON",
    "-DGMP_INCLUDE_DIR=/usr/include",
    "-DGMPXX_INCLUDE_DIR=/usr/include",
    "-DGMP_LIBRARIES=/usr/lib/libgmp.so",
    "-DGMPXX_LIBRARIES=/usr/lib/libgmpxx.so",
    "-DCaDiCaL_INCLUDE_DIR=/usr/include",
    "-DCaDiCaL_LIBRARIES=/usr/lib/libcadical.a",
    "-DSymFPU_INCLUDE_DIR=/usr/include",
    "-DMPFR_INCLUDE_DIR=/usr/include",
    "-DMPFR_LIBRARIES=/usr/lib/libmpfr.so",
    "-DENABLE_AUTO_DOWNLOAD=OFF",
    "-DUSE_PYTHON_VENV=OFF",
    "-DSKIP_SET_RPATH=ON",
    "-DUSE_POLY=OFF",
    "-DUSE_EDITLINE=ON",
    "-DUSE_MPFR=ON",
]
hostmakedepends = [
    "bash",
    "cmake",
    "ninja",
    "pkgconf",
    "python",
    "python-pexpect",
    "python-pyparsing",
    "python-tomli",
]
makedepends = [
    "cadical-devel",
    "cadical-devel-static",
    "gmp-devel",
    "gmp-gmpxx-devel",
    "libedit-devel",
    "mpfr-devel",
    "symfpu",
]
pkgdesc = "High-performance theorem prover and SMT solver"
license = "BSD-3-Clause"
url = "https://cvc5.github.io"
source = [
    f"https://github.com/cvc5/cvc5/archive/refs/tags/cvc5-{pkgver}.tar.gz",
]
sha256 = ["40e7a0d311ebd583972f412701a0f4bc325632bab74ca25f407b3acbb66db44e"]
# tests are heavy and require additional dependencies (Google Test, etc.)
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


@subpackage("cvc5-devel")
def _(self):
    return self.default_devel()
