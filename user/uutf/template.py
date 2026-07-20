pkgname = "uutf"
pkgver = "1.0.4"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib", "ocamlbuild"]
makedepends = ["ocaml"]
pkgdesc = "Non-blocking streaming Unicode codec for OCaml"
license = "ISC"
url = "https://erratique.ch/software/uutf"
source = f"https://erratique.ch/software/uutf/releases/uutf-{pkgver}.tbz"
sha256 = "a7a578e6af9149a8894e18e3b4759c8565937a69c6c9ace7a30bbf0484619ca8"
options = ["!cross", "!lintstatic"]


def build(self):
    self.do(
        "ocamlbuild",
        "-use-ocamlfind",
        "-classic-display",
        "-tags",
        "bin_annot,safe_string",
        "src/uutf.cma",
        "src/uutf.cmxa",
        "src/uutf.cmxs",
    )


def install(self):
    dest = "usr/lib/ocaml/uutf"
    self.install_dir(dest)

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
        p = self.cwd / "_build/src" / f"uutf.{ext}"
        if p.exists():
            self.install_file(f"_build/src/uutf.{ext}", dest)

    # Install META file for ocamlfind with version substitution
    meta_src = self.cwd / "pkg" / "META"
    meta_text = meta_src.read_text()
    meta_text = meta_text.replace("1.0.4", pkgver)
    meta_dst = self.destdir / dest / "META"
    meta_dst.write_text(meta_text)
    meta_dst.chmod(0o644)

    self.install_license("LICENSE.md")
