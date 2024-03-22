class CertificateCommand:
    def execute(self, *args, **kwargs):
        print("Executing Command 2")
        print(f"Args: {args}")
        print(f"Kwargs: {kwargs}")
