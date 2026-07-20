pkgname = "vampire"
pkgver = "5.0.1"
pkgrel = 0
build_style = "cmake"
# cadical, viras, z3 are git submodules of the upstream repo.
# GitHub archive tarballs do not include submodule content, so we fetch
# them separately and extract into the expected paths via source_paths.
_cadical_commit = "f13d74439a5b5c963ac5b02d05ce93a8098018b8"
_viras_commit = "a2ed173c65aca8d3189b5c6150914cd99adea1df"
_z3_commit = "3c47fd96cf5645d0c42b2c819d9e9a84380aa721"
configure_args = [
    # Must be a standard CMake build type (Release) rather than the cmake
    # build style default (None), because Vampire's subsat code asserts
    # (NDEBUG defined) == (VDEBUG == 0). CMake only defines NDEBUG for
    # the standard types (Release, MinSizeRel, etc.), and Vampire only
    # sets VDEBUG=1 when CMAKE_BUILD_TYPE is Debug.
    "-DCMAKE_BUILD_TYPE=Release",
]
hostmakedepends = [
    "cmake",
    "ninja",
    "python",
]
pkgdesc = "Automated theorem prover for first-order logic"
license = "BSD-3-Clause"
url = "https://vprover.github.io"
source = [
    f"https://github.com/vprover/vampire/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://github.com/arminbiere/cadical/archive/{_cadical_commit}.tar.gz",
    f"https://github.com/joe-hauns/viras/archive/{_viras_commit}.tar.gz",
    f"https://github.com/Z3Prover/z3/archive/{_z3_commit}.tar.gz",
]
source_paths = [".", "cadical", "viras", "z3"]
sha256 = [
    "8e4b09d782e9874fa6597d0bacc10fe80c209b3a0411ed018b078bb134c98c19",
    "ffeab40171153fb3064c7ccc0278f5d7e1772ebdf2da85a3bf19a3f5be7cf4b0",
    "81f1ae8365058028a8c95c6c4270526c27045105ebb720fc683d462e52f70c1a",
    "625347c1af4bc0077909188ab45b7a6367d3041d60b3778a761f3388a69c9d7c",
]
hardening = ["vis", "cfi"]
# Tests only run in Debug build (unit tests require the vtest executable
# which is only built in Debug mode)
options = ["!check"]


def pre_configure(self):
    # Build Z3 as a static library so Vampire's CMake picks it up.
    # Vampire's CMakeLists.txt looks for Z3 in ${CMAKE_SOURCE_DIR}/z3/build/
    # using find_package(Z3 CONFIG ...) with NO_SYSTEM_PATH.
    from cbuild.util import cmake

    with self.stamp("z3_configure") as s:
        s.check()
        cmake.configure(
            self,
            build_dir="z3/build",
            cmake_dir="z3",
            generator="Unix Makefiles",
            extra_args=[
                "-DZ3_SINGLE_THREADED=TRUE",
                "-DZ3_BUILD_LIBZ3_SHARED=FALSE",
                "-DCMAKE_BUILD_TYPE=Release",
            ],
        )

    with self.stamp("z3_build") as s:
        s.check()
        cmake.build(self, "z3/build")


def post_install(self):
    self.install_license("LICENCE")
