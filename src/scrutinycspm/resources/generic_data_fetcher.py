from abc import ABC, abstractmethod

class GenericDataFetcher(ABC):
    @abstractmethod
    def fetch_data(self):
        pass
