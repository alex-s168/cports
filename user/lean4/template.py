pkgname = "lean4"
pkgver = "4.32.0"
pkgrel = 0
build_style = "cmake"
configure_args = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DUSE_GITHASH=OFF",
    "-DINSTALL_LICENSE=OFF",
    "-DINSTALL_CADICAL=OFF",
    "-DINSTALL_LEANTAR=OFF",
    "-DUSE_MIMALLOC=OFF",
]
make_cmd = "make"
hostmakedepends = [
    "bash",
    "cadical",
    "cmake",
    "leangz",
    "pkgconf",
]
makedepends = [
    "gmp-devel",
    "libuv-devel",
    "openssl3-devel",
]
depends = ["cadical"]
pkgdesc = "Automatic and interactive theorem prover"
license = "Apache-2.0"
url = "https://lean-lang.org"
source = (
    f"https://github.com/leanprover/lean4/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "f39c6d87a9b4e9253bef15ffae460d2652b668e619688e4c01e59bbd2cd3b002"


def post_install(self):
    self.install_license("LICENSE")


@subpackage("lean4-devel")
def _(self):
    return [
        "usr/include",
        "usr/lib/lean/*.a",
    ]
