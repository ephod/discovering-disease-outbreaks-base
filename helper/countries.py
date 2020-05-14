import json
from typing import Dict, List

from geonamescache import GeonamesCache

from helper import Country, Place


class Countries(Place):
    def __init__(self, json_file: str, geonames_cache: GeonamesCache):
        super().__init__(json_file, geonames_cache)
        self.save_as_json()

    def save_as_json(self) -> None:
        if self.json_file_path.is_file():
            return
        # Create JSON file if file doesn't exist
        countries_ordered_by_word_count: Dict[int, List[str]] = {}
        for country in self.get_countries().values():
            country_name: str = country['name']
            word_count: int = len(country_name.split(" "))
            if word_count not in countries_ordered_by_word_count.keys():
                countries_ordered_by_word_count[word_count] = []
            countries_ordered_by_word_count[word_count].append(country_name)

        with self.json_file_path.open('w', encoding='utf8') as file_handler:
            # All int keys will be coerced to string keys
            # @url https://bugs.python.org/issue32816
            json.dump(countries_ordered_by_word_count, file_handler, ensure_ascii=False, sort_keys=True)

    def get_countries(self) -> Dict[str, Country]:
        return self.geonames_cache.get_countries()

    def load_json(self) -> Dict[int, List[str]]:
        data: Dict = {}
        with self.json_file_path.open(encoding='utf8') as file_handler:
            # All int keys will be coerced to string keys
            # @url https://bugs.python.org/issue32816
            data = json.load(file_handler)
        return {int(key): value for key, value in self.load_json().items()}
