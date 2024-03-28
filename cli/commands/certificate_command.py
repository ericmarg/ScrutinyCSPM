from cli.commands.command_manager import CommandPlugin

class CertificateCommand(CommandPlugin):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        arg1, arg2 = self.args
        return f"{arg1} {arg2}"

    def help(self):
        return "Usage: certificate <arg1> <arg2>\nThis command concatenates arg1 and arg2 and returns the result."