from abc import ABC, abstractmethod


class SchemaVersioner(ABC):
    @abstractmethod
    def get_schema_version(self) -> int:
        pass

    @abstractmethod
    def set_schema_version(self, v: int):
        pass
