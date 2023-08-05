from . import commands
import pkgutil
import importlib

# https://packaging.python.org/guides/creating-and-discovering-plugins/


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def load_commands():
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg in iter_namespace(commands)
    }
