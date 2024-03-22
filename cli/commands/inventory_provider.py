class ProviderCommand:
    def __init__(self, cfg, args):
        self.cfg = cfg
        self.args = args

    def execute(self):
        print("Executing Inventory Cmd Provider Cmd")
        print(f"Config: {self.cfg}")
        print(f"Arguments: {self.args}")