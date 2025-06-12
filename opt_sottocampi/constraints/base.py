from abc import ABC, abstractmethod

class BaseConstraint(ABC):
    @abstractmethod
    def apply(self, model, var_assignements, var_zone_in_sc, data):
        pass