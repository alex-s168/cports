pkgname = "cosmic-initial-setup"
pkgver = "1.3.0"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "just", "pkgconf"]
makedepends = [
    "libinput-devel",
    "libpulse-devel",
    "libxkbcommon-devel",
    "rust-std",
    "zstd-devel",
]
depends = ["cosmic-icon-theme", "polkit"]
pkgdesc = "COSMIC initial setup wizard"
license = "GPL-3.0-only"
url = "https://github.com/pop-os/cosmic-initial-setup"
source = f"{url}/archive/refs/tags/epoch-{pkgver}.tar.gz"
sha256 = "aeadf932dcf7d37681322af8822200edee3f91e5bef65b93f55492aa8ee9afc5"
# no tests
options = ["!check", "etcfiles"]


def init_build(self):
    # aws-lc-sys explicitly passes -Wa,--debug-prefix-map=old= for
    # assembly sources, but clang's integrated assembler rejects it.
    # Patch out the problematic asm_flag from the vendored builder.
    aws_build = (
        self.cwd / "vendor" / "aws-lc-sys-0.42.0" / "builder" / "cc_builder.rs"
    )
    if aws_build.exists():
        content = aws_build.read_text()
        if "debug-prefix-map" in content:
            content = content.replace(
                "\n            if cc_build.is_flag_supported(&asm_flag).unwrap_or(false) {\n                cc_build.asm_flag(asm_flag);\n            }",
                "",
            )
            aws_build.write_text(content)
            # Clear vendor checksums so cargo does not reject our change
            csum = (
                self.cwd
                / "vendor"
                / "aws-lc-sys-0.42.0"
                / ".cargo-checksum.json"
            )
            if csum.exists():
                txt = csum.read_text()
                pkg_start = txt.find('"package"')
                if pkg_start >= 0:
                    txt = '{"files":{},' + txt[pkg_start:]
                    csum.write_text(txt)


def install(self):
    _target_dir = f"target/{self.profile().triplet}"
    self.do(
        "just",
        f"rootdir={self.chroot_destdir}",
        f"cargo-target-dir={_target_dir}",
        "install",
    )
