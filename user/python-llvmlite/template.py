pkgname = "python-llvmlite"
pkgver = "0.48.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = [
    "cmake",
    "python-build",
    "python-installer",
    "python-setuptools",
    "python-wheel",
]
makedepends = [
    "llvm-devel",
    "python-devel",
]
depends = ["python"]
pkgdesc = "Lightweight LLVM Python binding"
license = "BSD-2-Clause AND Apache-2.0 WITH LLVM-exception"
url = "https://llvmlite.readthedocs.io"
source = f"$(PYPI_SITE)/l/llvmlite/llvmlite-{pkgver}.tar.gz"
sha256 = "543b19f9ef8f3c7c60d1468191e4ee1b1537bf9f8a3d56f64c0ddd98de92edd2"
env = {
    "LLVMLITE_SHARED": "ON",
}


def check(self):
    from cbuild.util import python

    pybin = python.setup_wheel_venv(self, ".cbuild-checkenv")
    self.do(
        pybin,
        "-c",
        "from llvmlite.tests import main; main()",
        path=[pybin.parent],
    )


def post_install(self):
    self.install_license("LICENSE")
    self.install_license("LICENSE.thirdparty")
