class InventoryCommand:
    def execute(self, *args, **kwargs):
        print("Executing Command 1")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")