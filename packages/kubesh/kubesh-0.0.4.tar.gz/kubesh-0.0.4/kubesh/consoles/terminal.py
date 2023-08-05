from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.formatters import TerminalFormatter
from pygments.lexers import YamlLexer
from prompt_toolkit import print_formatted_text, ANSI, HTML
from prompt_toolkit.styles import Style
from tabulate import tabulate
from pygments import highlight
import yaml


class TerminalConsole:
    def __init__(self, config_context):
        # Feed the autocompleter
        self.session = PromptSession()
        self.config_context = config_context
        self.toolbar_style = Style.from_dict(
            {
                "bottom-toolbar": "#aaaa00 bg:#ff0000",
                "bottom-toolbar.text": "#6A5ACD bg:#ffffff",
            }
        )

    def run(self):
        while True:
            command = self.session.prompt(
                ">> ",
                bottom_toolbar=self.get_toolbar,
                style=self.toolbar_style,
                refresh_interval=5,
                lexer=PygmentsLexer(YamlLexer),
            )
            if not command:  # Just skip empty enters
                continue
            short_cmd = command.split()[0]
            result = self.cmd_handler.process(command)
            if result == "not_found":
                print_formatted_text(
                    HTML(
                        f"Error: <ansired>Command '{short_cmd}' is not defined</ansired>"
                    )
                )
            if result == "quit":
                exit(0)

    def get_toolbar(self):
        cluster = self.config_context["context"]["cluster"]
        user = self.config_context["context"]["user"]
        user = user.split("/")[0]
        status = f" <b>{user}@{cluster}</b> "
        return HTML(status)

    def table(self, table_data):
        headers = table_data[0]
        values = table_data[1:]
        print_formatted_text(tabulate(values, headers=headers))

    def print_yaml(self, data):
        yaml_data = yaml.dump(data)
        print_formatted_text(
            ANSI(
                highlight((yaml_data), lexer=YamlLexer(), formatter=TerminalFormatter())
            )
        )

    def error(self, message):
        print_formatted_text(HTML(f"<ansired>{message}</ansired>"))
