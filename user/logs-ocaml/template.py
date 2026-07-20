pkgname = "logs-ocaml"
pkgver = "0.7.0"
pkgrel = 1
hostmakedepends = ["ocaml", "ocaml-findlib", "ocamlbuild"]
makedepends = ["fmt-ocaml-devel", "ocaml"]
pkgdesc = "Logging infrastructure for OCaml"
license = "ISC"
url = "https://erratique.ch/software/logs"
source = f"https://github.com/dbuenzli/logs/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "0aebc3f6ff751d319605a0150f3910ed7a858c36bf770c111c68711f0adf3732"
options = ["!cross", "!lintstatic"]


def build(self):
    self.do(
        "ocamlbuild",
        "-use-ocamlfind",
        "-classic-display",
        "logs.cma",
        "logs.cmxa",
        "logs.cmxs",
        "logs_fmt.cma",
        "logs_fmt.cmxa",
        "logs_fmt.cmxs",
    )


def install(self):
    # Install compiled library files to /usr/lib/ocaml/logs/
    dest = "usr/lib/ocaml/logs"
    self.install_dir(dest)

    # Build .a archives from .o files (ocamlopt -a doesn't produce .a on its own)
    for lib in ["logs", "logs_fmt"]:
        self.do(
            "ar",
            "rcs",
            f"_build/src/{lib}.a",
            f"_build/src/{lib}.o",
        )

    # Install built artifacts (excluding source files)
    for lib in ["logs", "logs_fmt"]:
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
            p = self.cwd / "_build/src" / f"{lib}.{ext}"
            if p.exists():
                self.install_file(f"_build/src/{lib}.{ext}", dest)

    # Install META file for ocamlfind with version substitution
    meta_src = self.cwd / "pkg" / "META"
    meta_text = meta_src.read_text()
    meta_text = meta_text.replace("%%VERSION_NUM%%", pkgver)
    meta_dst = self.destdir / dest / "META"
    meta_dst.write_text(meta_text)
    meta_dst.chmod(0o644)

    self.install_license("LICENSE.md")


@subpackage("logs-ocaml-devel")
def _(self):
    self.subdesc = "development files"
    self.depends = [self.parent]
    self.options = ["!lintstatic"]

    return [
        "usr/lib/ocaml/logs/*.a",
        "usr/lib/ocaml/logs/*.cmxa",
        "usr/lib/ocaml/logs/*.cmx",
        "usr/lib/ocaml/logs/*.cmi",
        "usr/lib/ocaml/logs/*.cmt",
        "usr/lib/ocaml/logs/*.cmti",
        "usr/lib/ocaml/logs/*.o",
    ]
