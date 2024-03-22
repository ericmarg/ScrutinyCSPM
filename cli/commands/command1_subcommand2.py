class Command1Subcommand2:
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args

    def execute(self):
        print("Executing Command 1 Subcommand 2")
        print(f"Config: {self.cfg}")
        print(f"Arguments: {self.args}")