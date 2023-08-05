class Command:
    callers = [".quit", ".q"]
    description = "Quit the current shell"

    def run(self, console, api):
        return "quit"
