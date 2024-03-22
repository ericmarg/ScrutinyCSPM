class Command1Subcommand1:
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args

    def execute(self):
        print("Executing Command 1 Subcommand 1")
        print(f"Config: {self.cfg}")
        print(f"Arguments: {self.args}")