class InventoryCommand:
    def execute(self, *args, **kwargs):
        print("Executing Inventory Command")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")