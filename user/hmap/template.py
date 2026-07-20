pkgname = "hmap"
pkgver = "0.8.1"
pkgrel = 0
hostmakedepends = ["ocaml", "ocaml-findlib", "ocamlbuild"]
makedepends = ["ocaml"]
pkgdesc = "Heterogeneous value maps for OCaml"
license = "ISC"
url = "http://erratique.ch/software/hmap"
source = f"http://erratique.ch/software/hmap/releases/hmap-{pkgver}.tbz"
sha256 = "6a00db1b12b6f55e1b2419f206fdfbaa669e14b51c78f8ac3cffa0a58897be83"
options = ["!cross", "!lintstatic"]


def configure(self):
    pass


def build(self):
    self.do(
        "ocamlbuild",
        "-use-ocamlfind",
        "-classic-display",
        "-tags",
        "bin_annot,safe_string",
        "src/hmap.cma",
        "src/hmap.cmxa",
        "src/hmap.cmxs",
    )


def install(self):
    dest = "usr/lib/ocaml/hmap"
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
        p = self.cwd / "_build/src" / f"hmap.{ext}"
        if p.exists():
            self.install_file(f"_build/src/hmap.{ext}", dest)

    # Install META file
    meta_src = self.cwd / "pkg" / "META"
    if meta_src.exists():
        meta_text = meta_src.read_text()
        meta_text = meta_text.replace("%%VERSION%%", pkgver)
        meta_dst = self.destdir / dest / "META"
        meta_dst.write_text(meta_text)
        meta_dst.chmod(0o644)

    self.install_license("LICENSE.md")
