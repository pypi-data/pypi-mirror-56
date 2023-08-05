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

    def process(self, command):
        handler = self.callers.get(command)
        if handler:
            return handler.run(self.console, self.api)
