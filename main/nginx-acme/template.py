pkgname = "nginx-acme"
pkgver = "0.4.1"
pkgrel = 0
build_style = "cargo"
make_env = {"NGINX_BUILD_DIR": "/usr/src/nginx/objs"}
hostmakedepends = [
    "cargo-auditable",
    "nginx-src",
    "pkgconf",
]
makedepends = [
    "clang-devel",
    "linux-headers",
    "openssl3-devel",
    "pcre2-devel",
    "rust-std",
]
depends = ["nginx"]
pkgdesc = "ACME client module for nginx"
license = "Apache-2.0"
url = "https://github.com/nginx/nginx-acme"
source = f"{url}/releases/download/v{pkgver}/nginx-acme-{pkgver}.tar.gz"
sha256 = "b4f99f971bd0bebc89b2037f3afeaa3281004fe434de558df87d69cab2be1f22"
file_modes = {
    "+usr/lib/nginx/modules": ("root", "root", 0o755, True),
}
# 'cargo check' does weird things, and seems like it doesn't build the shared library, and instead tries to link against nginx
options = ["etcfiles", "!check", "!cross"]


def install(self):
    self.install_file(
        f"target/{self.profile().triplet}/release/libnginx_acme.so",
        "usr/lib/nginx/modules",
        0o755,
    )
    modcp = self.destdir / "etc/nginx/modules"
    self.mkdir(modcp, parents=True)
    with open(modcp / "000_acme.conf", "w") as outf:
        outf.write('load_module "modules/libnginx_acme.so";\n')
    self.install_license("LICENSE")
