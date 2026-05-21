from abc import ABC, abstractmethod

import pyarrow as pa

from helpers import Table

class Extractor(ABC):
    @property
    @abstractmethod
    def schema(self) -> pa.schema:
        pass

    @abstractmethod
    def extract(self, data: dict, buffer: Table) -> None:
        pass