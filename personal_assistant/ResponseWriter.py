from abc import ABC, abstractmethod

class AbstractResponseWriter(ABC):

    @abstractmethod
    def write(self, output: str):
        pass

class ConsoleResponseWriter(AbstractResponseWriter):
    def write(self, output: str):
        print(output)