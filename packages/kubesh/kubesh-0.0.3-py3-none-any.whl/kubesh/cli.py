import sys
import click
from . import __version__
from .plugins import load_commands
from .consoles import TerminalConsole, StdinConsole
from .cmd_handler import CommandHandler
from .api import get_api, config


@click.command()
@click.version_option(version=__version__)
def main():
    try:
        api = get_api()
    except TypeError:
        print("ERROR: Unable to find KUBECONFIG file !!!")
        exit(2)
    commands = load_commands()
    console_class = TerminalConsole if sys.stdin.isatty() else StdinConsole
    console = console_class(config.list_kube_config_contexts()[1])
    CommandHandler(commands, console, api)
    console.run()
