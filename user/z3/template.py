pkgname = "z3"
pkgver = "5.0.0"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DZ3_INCLUDE_GIT_DESCRIBE=OFF",
    "-DZ3_INCLUDE_GIT_HASH=OFF",
    "-DZ3_BUILD_PYTHON_BINDINGS=OFF",
    "-DZ3_BUILD_LIBZ3_SHARED=ON",
]
hostmakedepends = ["cmake", "ninja", "pkgconf", "python"]
pkgdesc = "High-performance theorem prover and SMT solver"
license = "MIT"
url = "https://github.com/Z3Prover/z3"
source = f"https://github.com/Z3Prover/z3/archive/refs/tags/z3-{pkgver}.tar.gz"
sha256 = ["f3bf2274e61f22417c7354613cb57d4f8de86067029db1771523d7c34d27bf4c"]
hardening = ["vis", "cfi"]


def check(self):
    from cbuild.util import cmake

    cmake.build(self, self.make_dir, ["--target", "test-z3"])
    self.do("./test-z3", "/a", wrksrc=self.make_dir)


def post_install(self):
    self.install_license("LICENSE.txt")


@subpackage("z3-devel")
def _(self):
    return self.default_devel()
