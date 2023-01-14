from abc import ABC, abstractmethod, abstractclassmethod

STEPS = {}

def register(klass):
    STEPS[klass.step_name()] = klass

class Step(ABC):

    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def run(self) -> bool:
        """Returns true if runbook can continue."""
        pass

    @abstractmethod
    def get_step_detail(self) -> str:
        pass

    @abstractclassmethod
    def step_name(cls) -> str:
        pass
