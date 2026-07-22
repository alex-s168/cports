pkgname = "leangz"
pkgver = "0.1.19"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf"]
makedepends = ["rust-std", "zstd-devel"]
pkgdesc = "Lean 4 .olean file compressor and decompressor"
license = "Apache-2.0"
url = "https://github.com/digama0/leangz"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "209b1d2408f82ab4eaea656097a34535f7a3a005195d482becde00b0b4b3b1d6"


def install(self):
    self.install_bin(f"target/{self.profile().triplet}/release/leangz")
    self.install_bin(f"target/{self.profile().triplet}/release/leantar")
    self.install_license("LICENSE")
