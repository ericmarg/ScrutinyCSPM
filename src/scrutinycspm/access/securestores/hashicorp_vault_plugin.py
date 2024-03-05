import secure_plugin_base

class AwsSecureStorePlugin(secure_plugin_base.SecurePluginBase):
    def __init__(self, *args, **kwargs):
        pass

    def get_provider_name(self):
        return "aws"

    def store_secret(self, name, value):
        pass

    def retrieve_secret(self, name):
        pass

    def list_providers(self):
        pass

    def authenticate(self, *args, **kwargs):
        pass
