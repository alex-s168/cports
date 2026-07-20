from cbuild.util import dune as dune_util


def configure(self):
    pass


def build(self):
    self.dune.build()


def check(self):
    self.dune.check()


def install(self):
    self.dune.install()


def use(tmpl):
    tmpl.configure = configure
    tmpl.build = build
    tmpl.check = check
    tmpl.install = install

    tmpl.dune = dune_util.Dune(tmpl)
