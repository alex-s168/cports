class Dune:
    def __init__(self, tmpl, wrksrc=None):
        self.template = tmpl
        self.wrksrc = wrksrc
        self._override_pkgname = None

    def _pkgname(self):
        """Return the dune package name (can differ from Chimera pkgname)."""
        if self._override_pkgname is not None:
            return self._override_pkgname
        return self.template.pkgname

    def _invoke(self, command, args, env, wrksrc, wrapper, ewrapper):
        tmpl = self.template

        if not wrksrc:
            wrksrc = self.wrksrc
        if not wrksrc:
            wrksrc = tmpl.make_dir

        renv = dict(tmpl.make_env)
        renv.update(env)

        return tmpl.do(
            *wrapper,
            *ewrapper,
            "dune",
            command,
            *args,
            env=renv,
            wrksrc=wrksrc,
        )

    def build(self, args=[], env={}, wrksrc=None, wrapper=[]):
        tmpl = self.template
        return self._invoke(
            "build",
            [
                "-p",
                self._pkgname(),
                "-j",
                str(tmpl.make_jobs),
                *tmpl.make_build_args,
                *args,
                "@install",
            ],
            env,
            wrksrc,
            wrapper,
            tmpl.make_build_wrapper,
        )

    def check(self, args=[], env={}, wrksrc=None, wrapper=[]):
        tmpl = self.template
        return self._invoke(
            "build",
            [
                "-p",
                self._pkgname(),
                "-j",
                str(tmpl.make_jobs),
                *tmpl.make_check_args,
                *args,
                "@runtest",
            ],
            env,
            wrksrc,
            wrapper,
            tmpl.make_check_wrapper,
        )

    def install(self, args=[], env={}, wrksrc=None, wrapper=[]):
        tmpl = self.template
        pn = self._pkgname()
        return self._invoke(
            "install",
            [
                "-p",
                pn,
                "--create-install-files",
                pn,
                "--prefix",
                "/usr",
                *tmpl.make_install_args,
                *args,
            ],
            {"DESTDIR": str(tmpl.chroot_destdir), **tmpl.make_install_env, **env},
            wrksrc,
            wrapper,
            tmpl.make_install_wrapper,
        )
