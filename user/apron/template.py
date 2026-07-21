pkgname = "apron"
pkgver = "0.9.15"
pkgrel = 1
# no build_style: apron uses a custom shell configure script, not autoconf
hostmakedepends = ["camlidl", "ocaml", "ocaml-findlib", "ocamlbuild", "perl"]
makedepends = [
    "gmp-devel",
    "gmp-gmpxx-devel",
    "mlgmpidl",
    "mpfr-devel",
    "ocaml",
]
depends = ["mlgmpidl", "ocaml-runtime"]
ignore_shlibs = [
    "libapron_debug.so",
    "libboxD_debug.so",
    "libboxMPFR_debug.so",
    "libboxMPQ_debug.so",
    "liboctD_debug.so",
    "liboctMPQ_debug.so",
    "libpolkaMPQ_debug.so",
    "libpolkaRll_debug.so",
    "libt1pD_debug.so",
    "libt1pMPFR_debug.so",
    "libt1pMPQ_debug.so",
    "libavoD_debug.so",
    "libavoMPQ_debug.so",
]
pkgdesc = "Numerical abstract domain library for static analysis"
license = "LGPL-2.0-only"
url = "https://github.com/antoinemine/apron"
source = (
    f"https://github.com/antoinemine/apron/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "5778fa1afaf0b36fe6a79989fc4374b0b3ece8a5e46a7ab195440209ccd67b1b"
# tests disabled - test infrastructure requires additional unported dependencies
options = ["!cross", "!check", "!lintstatic"]


def configure(self):
    self.do(
        "./configure",
        "-prefix",
        "/usr",
        "-no-cxx",
        "-no-java",
        "-no-ppl",
        "-no-pplite",
        "-no-glpk",
    )


def build(self):
    self.do("make", "all")


def install(self):
    dest_prefix = str(self.chroot_destdir / "usr")
    ocaml_dir = "usr/lib/ocaml/apron"
    stublibs = "usr/lib/ocaml/stublibs"
    # Generate META file from META.in
    self.do("make", "ml")
    # Install C libraries/headers to DESTDIR (OCAMLFIND="" avoids host
    # ocamlfind install, C lib subdirs still install via APRON_PREFIX)
    self.do(
        "make",
        "install",
        f"APRON_PREFIX={dest_prefix}",
        "OCAMLFIND=",
    )
    # Remove debug C libraries and OCaml stubs that would confuse the
    # SONAME scanner; they are built unconditionally by the build system
    self.do(
        "sh",
        "-c",
        f"rm -f {dest_prefix}/lib/*_debug*"
        f" {dest_prefix}/lib/ocaml/apron/*_debug*",
    )
    # Install dll*.so to stublibs for bytecode dynamic loading
    self.install_dir(stublibs)
    for subdir in [
        "mlapronidl",
        "box",
        "octagons",
        "newpolka",
        "taylor1plus",
        "avoct",
    ]:
        p = self.cwd / subdir
        if not p.is_dir():
            continue
        for f in sorted(p.glob("dll*.so")):
            self.install_file(str(f.relative_to(self.cwd)), stublibs)
    # Set up OCaml findlib layout: copy all OCaml artifacts to
    # /usr/lib/ocaml/apron/ so downstream dune/ocamlfind can find them
    self.install_dir(ocaml_dir)
    self.install_file("mlapronidl/META", ocaml_dir)
    ocaml_exts = {".cma", ".cmxa", ".cmx", ".cmi", ".a", ".cmxs", ".idl"}
    for subdir in [
        "mlapronidl",
        "box",
        "octagons",
        "newpolka",
        "taylor1plus",
        "avoct",
    ]:
        p = self.cwd / subdir
        if not p.is_dir():
            continue
        for f in sorted(p.iterdir()):
            if f.suffix in ocaml_exts:
                self.install_file(str(f.relative_to(self.cwd)), ocaml_dir)


def post_install(self):
    self.install_license("COPYING")
