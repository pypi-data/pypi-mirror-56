from abc import ABC, abstractmethod


class Migration(ABC):
    @abstractmethod
    def from_version(self) -> int:
        pass

    def to_version(self) -> int:
        return self.from_version() + 1

    @abstractmethod
    def execute(self):
        pass
