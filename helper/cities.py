import json
from typing import Dict, Set, List

from geonamescache import GeonamesCache

from helper import City, Place


class Cities(Place):
    def __init__(self, json_file: str, geonames_cache: GeonamesCache):
        super().__init__(json_file, geonames_cache)
        self.save_as_json()

    def save_as_json(self) -> None:
        if self.json_file_path.is_file():
            return
        # Create JSON file if file doesn't exist
        cities_ordered_by_word_count: Dict[int, Set[str]] = {}
        for city in self.get_cities().values():
            city_name: str = city['name']
            country_code: str = city['countrycode']
            word_count: int = len(city_name.split(" "))
            if word_count not in cities_ordered_by_word_count.keys():
                cities_ordered_by_word_count[word_count] = set()
            cities_ordered_by_word_count[word_count].update([f"{city_name} {country_code}"])

        # Set is not JSON serializable
        json_data: Dict[int, List[str]] = {key: list(value) for key, value in cities_ordered_by_word_count.items()}

        with self.json_file_path.open('w', encoding='utf8') as file_handler:
            # All int keys will be coerced to string keys
            # @url https://bugs.python.org/issue32816
            json.dump(json_data, file_handler, ensure_ascii=False, sort_keys=True)

    def get_cities(self) -> Dict[str, City]:
        return self.geonames_cache.get_cities()

    def load_json(self) -> Dict[int, List[str]]:
        data: Dict = {}
        with self.json_file_path.open(encoding='utf8') as file_handler:
            # All int keys will be coerced to string keys
            # @url https://bugs.python.org/issue32816
            data = json.load(file_handler)
        return {int(key): value for key, value in data.items()}
