pkgname = "zarith_stubs_js"
pkgver = "0.17.0"
pkgrel = 0
build_style = "dune"
hostmakedepends = ["dune", "ocaml", "ocaml-findlib"]
makedepends = ["ocaml"]
depends = ["ocaml-runtime"]
pkgdesc = "Javascript stubs for the Zarith library"
license = "MIT"
url = "https://github.com/janestreet/zarith_stubs_js"
source = f"https://github.com/janestreet/zarith_stubs_js/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "7301b11007bde9dc113f694059b1ba994232752655d926403d7664eff3ae143a"
# no test suite; @runtest alias does not exist
options = ["!cross", "!check", "!lintstatic"]


def install(self):
    self.do(
        "dune",
        "install",
        "-p",
        "zarith_stubs_js",
        "--prefix",
        "/usr",
        "--libdir",
        "/usr/lib",
        "--docdir",
        "/usr/share/doc",
        env={**self.make_env, "DESTDIR": str(self.chroot_destdir)},
    )


def post_install(self):
    self.install_license("LICENSE.md")
