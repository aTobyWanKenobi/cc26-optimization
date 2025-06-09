from abc import ABC, abstractmethod

class BaseConstraint(ABC):
    @abstractmethod
    def apply(self, model, variables, data):
        pass