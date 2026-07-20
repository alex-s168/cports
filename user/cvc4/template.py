pkgname = "cvc4"
pkgver = "1.8"
pkgrel = 0
build_style = "cmake"
configure_args = ["-DCMAKE_BUILD_TYPE=Production"]
hostmakedepends = [
    "bash",
    "cmake",
    "git",
    "java-common",
    "ninja",
    "pkgconf",
    "python",
]
makedepends = [
    "gmp-devel",
    "gmp-gmpxx-devel",
    "libantlr3c",
    "libantlr3c-devel",
]
depends = ["gmp", "libantlr3c"]
pkgdesc = "High-performance theorem prover and SMT solver"
license = "BSD-3-Clause"
url = "https://cvc4.github.io"
source = [
    f"https://github.com/CVC4/CVC4-archived/archive/refs/tags/{pkgver}.tar.gz",
    "!https://www.antlr3.org/download/antlr-3.4-complete.jar",
]
sha256 = [
    "80fd10d5e4cca56367fc5398ba0117a86d891e0b9b247a97cd981fe02e8167f5",
    "9d3e866b610460664522520f73b81777b5626fb0a282a5952b9800b751550bf7",
]
# tests are heavy and require additional dependencies (CxxTest etc.)
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")


def init_configure(self):
    # Install Python helper for template substitution (used by
    # fix-mkexpr-subst.patch for Bash 5.3 compatibility)
    pyhelper = self.cwd / "subst_helper.py"
    pyhelper.write_text(
        "import os,sys\n"
        "v=sys.argv[1];t=sys.stdin.read();"
        "sys.stdout.write(t.replace('${'+v+'}',os.environ[v]))"
    )
    # Fix missing size_t and fpu_control on musl + Clang 22
    _fixes = {
        "src/expr/emptyset.h": (
            "#pragma once\n",
            "#pragma once\n#include <cstddef>\n",
        ),
        "src/expr/expr_iomanip.h": (
            "#ifndef CVC4__",
            "#include <cstddef>\n#ifndef CVC4__",
        ),
        "src/util/regexp.h": (
            "#ifndef CVC4__",
            "#include <cstddef>\n#ifndef CVC4__",
        ),
        "src/expr/node.h": (
            "#ifndef CVC4__",
            "#include <cstddef>\n#ifndef CVC4__",
        ),
        "src/prop/minisat/utils/System.h": (
            "#if defined(__linux__)",
            "#if defined(__linux__) && defined(__GLIBC__)",
        ),
        "src/prop/bvminisat/utils/System.h": (
            "#if defined(__linux__)",
            "#if defined(__linux__) && defined(__GLIBC__)",
        ),
    }
    for _hdr, (_old, _new) in _fixes.items():
        _c = (self.cwd / _hdr).read_text()
        _c = _c.replace(_old, _new)
        (self.cwd / _hdr).write_text(_c)
    # Create antlr3 wrapper script that cmake's FindANTLR.cmake can find
    antlr_jar = f"/sources/{self.pkgname}-{self.pkgver}/antlr-3.4-complete.jar"
    wrapper = self.wrapperdir / "antlr3"
    wrapper.write_text("#!/bin/sh\n" + f'exec java -jar {antlr_jar} "$@"\n')
    wrapper.chmod(0o755)


@subpackage("cvc4-devel")
def _(self):
    return self.default_devel()
