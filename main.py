# Builtin Python modules
import itertools
import json
from pathlib import Path
from pprint import pprint
import re
import string
from typing import Dict, List, Set

from geonamescache import GeonamesCache
from more_itertools import partitions

from helper import Cities, Countries, City, Country

# Cities
helper_cities = Cities("./data/cities.json", GeonamesCache())
group_cities_by_word_count: Dict[int, List[str]] = helper_cities.load_json()
cities: Dict[str, City] = helper_cities.get_cities()

# Countries
helper_countries = Countries("./data/countries.json", GeonamesCache())
group_countries_by_word_count: Dict[int, List[str]] = helper_countries.load_json()
countries: Dict[str, Country] = helper_countries.get_countries()

text_file: Path = Path('./data/headlines.txt')
assert text_file.is_file(), f"Wrong file: {text_file}"

unique_cities: Set[str] = set()
cities_country_code: Dict[str, List[str]] = {}
valid_characters: Set[str] = set([str(character) for character in [*string.ascii_letters, *string.digits]])
for city in cities.values():
    # Country code as dictionary key
    country_code = city['countrycode']
    if country_code not in cities_country_code.keys():
        cities_country_code[country_code] = []
    # Append city name
    city_name = city['name']
    if city_name not in cities_country_code[country_code]:
        cities_country_code[country_code].append(city_name)
        unique_cities.update([city_name])
        for character in city_name:
            valid_characters.update([character])
        country_name = countries[country_code]['name']
        for character in country_name:
            valid_characters.update([character])

lines: List[str] = []  # 650 lines
all_characters: Set[str] = set()
with text_file.open() as file_handler:
    for line in file_handler.readlines():
        current_line = line.rstrip('\n')
        lines.append(current_line)
        for character in current_line:
            all_characters.update([character])

nonvalid_characters: Set[str] = all_characters - valid_characters
nonvalid_translation: str = "".join(list(nonvalid_characters))
# Python's 3 compatibility
translation_table = dict.fromkeys(map(ord, nonvalid_translation), None)

for line in lines:
    # Remove unwanted characters
    current_line = line.translate(translation_table)
    # Remove multiple spaces
    current_line = re.sub(r"\s\s+", " ", current_line)
    words = current_line.split(" ")
    word_count = len(words)
    print(f"Line: {line}")
    unique_search_terms: Dict[int, Set[str]] = {}
    for partition in partitions(words):
        for subpartition in partition:
            subpartition_word_count: int = len(subpartition)
            if subpartition_word_count not in unique_search_terms.keys():
                unique_search_terms[subpartition_word_count] = set()
            search_term = " ".join(subpartition)
            unique_search_terms[subpartition_word_count].update([search_term])
    pprint(unique_search_terms)
    break
