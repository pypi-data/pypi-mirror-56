""" Command handler """
import inspect


class CommandHandler:
    def __init__(self, commands, console, api):
        self.commands = commands
        self.console = console
        self.api = api
        self.callers = {}
        for module_name, module_obj in commands.items():
            cls_members = inspect.getmembers(module_obj, inspect.isclass)
            cls_members = [
                c[1] for c in cls_members if c[1].__name__.startswith("Command")
            ]
            for cmd in cls_members:
                cmd_obj = cmd()
                for caller in cmd.callers:
                    assert caller not in self.callers
                    self.callers[caller] = cmd_obj
        # Ugly but we need so that console can call us
        console.cmd_handler = self

    def tokenizer(self, command):
        # it may need to be extended in the future
        # to handle more complex syntax options
        command = command.strip()
        tokens = command.split()
        return tokens

    def process(self, command):
        tokens = self.tokenizer(command)
        command = tokens[0]
        args = [] if len(tokens) < 2 else tokens[1:]
        handler = self.callers.get(command)
        if handler:
            return handler.run(self.console, self.api, args)
        return "not_found"

    @property
    def all_commands(self):

        # Reduce to unique command objects : https://stackoverflow.com/a/26043525/401041
        unique_commands = {x for x in self.callers.values()}

        # Reduce to the command name
        sorted_commands = sorted([cmd.callers[0] for cmd in unique_commands])

        # Return the cmd object for each command name
        return [self.callers[cmd_name] for cmd_name in sorted_commands]
