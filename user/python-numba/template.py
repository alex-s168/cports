pkgname = "python-numba"
pkgver = "0.66.0"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = [
    "python-build",
    "python-installer",
    "python-setuptools",
    "python-wheel",
]
makedepends = [
    "libomp-devel",
    "python-devel",
    "python-numpy-devel",
]
depends = ["python-numpy", "python-llvmlite"]
checkdepends = ["python-numpy-tests", "python-pytest", *depends]
pkgdesc = "Just-in-time compiler for numerical Python"
license = "BSD-3-Clause"
url = "https://numba.pydata.org"
source = f"$(PYPI_SITE)/n/numba/numba-{pkgver}.tar.gz"
sha256 = "b900e63a0e26c05ea9a6d5a3a5a0a177cb64c5011887bf43edb8c3ed2c38d363"


def check(self):
    from cbuild.util import python

    envpy = python.setup_wheel_venv(self, ".cbuild-checkenv")
    # Run the tests directly affected by the NumPy 2.5 compatibility patch.
    self.do(
        envpy,
        "-m",
        "pytest",
        "--pyargs",
        "numba.tests.test_dyn_array",
        "numba.tests.test_linalg",
        "numba.tests.test_np_functions",
        "numba.tests.test_npdatetime",
        "numba.tests.test_numpy_support",
        "numba.tests.test_polynomial",
        wrksrc=f"{self.chroot_cwd}/.cbuild-checkenv",
        path=[envpy.parent],
    )


def post_install(self):
    self.install_license("LICENSE")
    self.install_license("LICENSES.third-party")
