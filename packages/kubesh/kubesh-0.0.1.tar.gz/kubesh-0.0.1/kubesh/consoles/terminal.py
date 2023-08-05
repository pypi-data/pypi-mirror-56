from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.data import YamlLexer
from prompt_toolkit import print_formatted_text, HTML
from tabulate import tabulate


class TerminalConsole:
    def __init__(self):
        # Feed the autocompleter
        self.session = PromptSession()

    def run(self):
        while True:
            command = self.session.prompt(
                ">> ",
                bottom_toolbar=self.get_toolbar,
                refresh_interval=5,
                lexer=PygmentsLexer(YamlLexer),
            )
            if not command:  # Just skip empty enters
                continue
            short_cmd = command.split()[0]
            result = self.cmd_handler.process(command)
            if result is None:
                print_formatted_text(
                    HTML(
                        f"Error: <ansired>Command '{short_cmd}' is not defined</ansired>"
                    )
                )

    def get_toolbar(self):
        return "ok"

    def table(self, table_data):
        headers = table_data[0]
        values = table_data[1:]
        print_formatted_text(tabulate(values, headers=headers))
