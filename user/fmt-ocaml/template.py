pkgname = "fmt-ocaml"
pkgver = "0.9.0"
pkgrel = 1
hostmakedepends = ["ocaml", "ocaml-findlib", "ocamlbuild"]
makedepends = ["ocaml"]
pkgdesc = "OCaml Format pretty-printing combinators"
license = "ISC"
url = "https://erratique.ch/software/fmt"
source = f"https://github.com/dbuenzli/fmt/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "af0906f0665e76be69992c1a556c5ffc2f79d88d3ba6115d6abf21c0909c378c"
options = ["!cross", "!lintstatic"]


def build(self):
    self.do(
        "ocamlbuild",
        "-use-ocamlfind",
        "-classic-display",
        "-tags",
        "bin_annot,safe_string",
        "src/fmt.cma",
        "src/fmt.cmxa",
        "src/fmt.cmxs",
    )
    self.do(
        "ocamlbuild",
        "-use-ocamlfind",
        "-classic-display",
        "-tags",
        "bin_annot,safe_string",
        "-package",
        "unix",
        "src/fmt_tty.cma",
        "src/fmt_tty.cmxa",
        "src/fmt_tty.cmxs",
    )


def install(self):
    dest = "usr/lib/ocaml/fmt"
    self.install_dir(dest)

    # Build .a archives from .o files (ocamlopt -a doesn't produce .a on its own)
    for lib in ["fmt", "fmt_tty"]:
        self.do(
            "ar",
            "rcs",
            f"_build/src/{lib}.a",
            f"_build/src/{lib}.o",
        )

    for ext in [
        "cma",
        "cmxa",
        "cmxs",
        "cmi",
        "cmo",
        "cmx",
        "cmt",
        "cmti",
        "a",
        "o",
    ]:
        for lib in ["fmt", "fmt_tty"]:
            p = self.cwd / "_build/src" / f"{lib}.{ext}"
            if p.exists():
                self.install_file(f"_build/src/{lib}.{ext}", dest)

    # Install top init file
    self.install_file("src/fmt_tty_top_init.ml", dest)

    # Install META file for ocamlfind with version substitution
    meta_src = self.cwd / "pkg" / "META"
    meta_text = meta_src.read_text()
    meta_text = meta_text.replace("%%VERSION_NUM%%", pkgver)
    meta_dst = self.destdir / dest / "META"
    meta_dst.write_text(meta_text)
    meta_dst.chmod(0o644)

    self.install_license("LICENSE.md")


@subpackage("fmt-ocaml-devel")
def _(self):
    self.subdesc = "development files"
    self.depends = [self.parent]
    self.options = ["!lintstatic"]

    return [
        "usr/lib/ocaml/fmt/*.a",
        "usr/lib/ocaml/fmt/*.cmxa",
        "usr/lib/ocaml/fmt/*.cmx",
        "usr/lib/ocaml/fmt/*.cmi",
        "usr/lib/ocaml/fmt/*.cmt",
        "usr/lib/ocaml/fmt/*.cmti",
        "usr/lib/ocaml/fmt/*.o",
    ]
