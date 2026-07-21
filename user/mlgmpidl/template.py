pkgname = "mlgmpidl"
pkgver = "1.3.0"
pkgrel = 1
hostmakedepends = ["camlidl", "clang", "ocaml", "ocaml-findlib", "perl"]
makedepends = ["bigarray-compat", "camlidl", "gmp-devel", "mpfr-devel", "ocaml"]
depends = ["bigarray-compat", "ocaml-runtime"]
pkgdesc = "OCaml interface to the GMP library"
license = "LGPL-2.1-only WITH OCaml-LGPL-linking-exception"
url = "https://github.com/nberth/mlgmpidl"
source = f"https://github.com/nberth/mlgmpidl/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "51a25f51068b1439ae71469ae506b1637d4e6f782a00955317bdff0f41ec49f8"
options = ["!cross", "!lintstatic"]


def configure(self):
    # mlgmpidl's Makefile hardcodes 'cpp' for preprocessing IDL files.
    # On Chimera, clang-cpp provides the C preprocessor.
    if not (self.cwd / "cpp").exists():
        (self.cwd / "cpp").symlink_to("/usr/bin/clang-cpp")
    self.do(
        "./configure",
        "--prefix",
        "/usr",
    )


def build(self):
    # Ensure the build dir is first in PATH so the 'cpp' symlink is found
    self.do("make", env={"PATH": "/builddir/mlgmpidl-1.3.0:/usr/bin:/bin"})


def check(self):
    pass


def install(self):
    destdir = str(self.chroot_destdir)
    # Generate META file
    self.do("make", "META")
    # Ensure the install directory exists
    self.install_dir("usr/lib/ocaml")
    # Build the shared stublib for bytecode dynamic loading
    # Use libgmp_caml.a directly since it's a static archive linking
    # into a shared library; use whole-archive to pull in all objects.
    self.do(
        "clang",
        "-shared",
        "-o",
        "dllgmp_caml.so",
        "-fPIC",
        "-Wl,--whole-archive",
        "libgmp_caml.a",
        "-Wl,--no-whole-archive",
        "-lmpfr",
        "-lgmp",
        "/usr/lib/ocaml/libcamlidl.a",
    )
    # Install via ocamlfind with destdir
    self.do(
        "ocamlfind",
        "install",
        "-destdir",
        f"{destdir}/usr/lib/ocaml",
        "-ldconf",
        "/dev/null",
        "gmp",
        "META",
        "gmp_caml.h",
        "gmp.cma",
        "gmp.cmxa",
        "gmp.a",
        "libgmp_caml.a",
        "dllgmp_caml.so",
    )
    # Also install to stublibs so the bytecode runtime can find it
    self.install_dir("usr/lib/ocaml/stublibs")
    self.install_file("dllgmp_caml.so", "usr/lib/ocaml/stublibs")
    # Install the remaining files via glob
    for ext in ["cmi", "cmx", "ml", "mli", "idl"]:
        self.install_file(f"*.{ext}", "usr/lib/ocaml/gmp", glob=True)


def post_install(self):
    self.install_license("COPYING")
