from abc import ABC, abstractmethod
from collections import defaultdict

import requests

Table = dict[str, list]

class Reference(ABC):
    url: str
    data: dict
    table: Table

    def __init__(self, url: str):
        self.url = url
        self.data = {}
        self.table = defaultdict(list)

    def get_data(self) -> None:
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            raise Exception(f"Failed to fetch data from {self.url}. Status code: {response.status_code}")

    @abstractmethod
    def extract(self) -> Table:
        pass