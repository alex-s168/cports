pkgname = "vampire"
pkgver = "5.0.1"
pkgrel = 1
build_style = "cmake"
# cadical and viras are git submodules of the upstream repo.
# GitHub archive tarballs do not include submodule content, so we fetch
# them separately and extract into the expected paths via source_paths.
_cadical_commit = "f13d74439a5b5c963ac5b02d05ce93a8098018b8"
_viras_commit = "a2ed173c65aca8d3189b5c6150914cd99adea1df"
configure_args = [
    # Must be a standard CMake build type (Release) rather than the cmake
    # build style default (None), because Vampire's subsat code asserts
    # (NDEBUG defined) == (VDEBUG == 0). CMake only defines NDEBUG for
    # the standard types (Release, MinSizeRel, etc.), and Vampire only
    # sets VDEBUG=1 when CMAKE_BUILD_TYPE is Debug.
    "-DCMAKE_BUILD_TYPE=Release",
    # Point to system z3; Vampire's CMakeLists.txt uses NO_* path flags
    # that block system paths by default.
    "-DZ3_DIR=/usr/lib/cmake/z3",
]
hostmakedepends = [
    "cmake",
    "ninja",
    "python",
]
makedepends = ["z3-devel"]
pkgdesc = "Automated theorem prover for first-order logic"
license = "BSD-3-Clause"
url = "https://vprover.github.io"
source = [
    f"https://github.com/vprover/vampire/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://github.com/arminbiere/cadical/archive/{_cadical_commit}.tar.gz",
    f"https://github.com/joe-hauns/viras/archive/{_viras_commit}.tar.gz",
]
source_paths = [".", "cadical", "viras"]
sha256 = [
    "8e4b09d782e9874fa6597d0bacc10fe80c209b3a0411ed018b078bb134c98c19",
    "ffeab40171153fb3064c7ccc0278f5d7e1772ebdf2da85a3bf19a3f5be7cf4b0",
    "81f1ae8365058028a8c95c6c4270526c27045105ebb720fc683d462e52f70c1a",
]
hardening = ["vis", "cfi"]
# Tests only run in Debug build (unit tests require the vtest executable
# which is only built in Debug mode)
options = ["!check"]


def post_install(self):
    self.install_license("LICENCE")
