from abc import ABC, abstractmethod

class LLMClient(ABC):

    @abstractmethod
    def chat(self, messagee: str) -> str:
        pass
