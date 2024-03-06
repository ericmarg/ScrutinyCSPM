import abc

class SecurePluginBase(abc.ABC):

    @abc.abstractmethod
    def get_provider_name(self):
        """Return secret provider name """
        pass

    @abc.abstractmethod
    def store_secret(self, *args, **kwargs):
        """Store secret in backend provider"""
        pass

    @abc.abstractmethod
    def retrieve_secret(self, name):
        """Get secret value from storage"""
        pass

    @abc.abstractmethod
    def list_providers(self):
        """List all secret providers"""
        pass

    def authenticate(self, *args, **kwargs):
        """Authenticate into the secure store"""
        pass