from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from geonamescache import GeonamesCache


class Place(ABC):
    json_file_path: Path
    geonames_cache: GeonamesCache

    def __init__(self, json_file_path: str, geonames_cache: GeonamesCache) -> None:
        # File path
        self.json_file_path = Path(json_file_path)
        json_extension = '.json'
        if self.json_file_path.suffix != json_extension:
            raise AssertionError(f"Wrong extension. JSON file expected: {self.json_file_path}")
        # GeonamesCache dependency
        self.geonames_cache = geonames_cache
        class_name = "GeonamesCache"
        if self.geonames_cache.__class__.__name__ != class_name:
            raise AssertionError(f"Wrong class. Class expected: {class_name}")
        super().__init__()

    @abstractmethod
    def save_as_json(self) -> None:
        pass

    @abstractmethod
    def load_json(self) -> Dict[int, List[str]]:
        pass
