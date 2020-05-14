# Builtin Python modules
import csv
from pathlib import Path
import re
import string
from typing import Dict, List, Set
import unicodedata

from geonamescache import GeonamesCache
from more_itertools import partitions
import pandas as pd

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
map_country_code_to_city: Dict[str, List[str]] = {}

extra_characters = ["-", "’", "/"]
valid_characters: Set[str] = set(
    [str(character) for character in [*string.ascii_letters, *string.digits, *extra_characters]])

for city in cities.values():
    # Country code as dictionary search_term_length
    country_code = city['countrycode']
    if country_code not in map_country_code_to_city.keys():
        map_country_code_to_city[country_code] = []
    # Append city name
    city_name = city['name']
    if city_name not in map_country_code_to_city[country_code]:
        map_country_code_to_city[country_code].append(city_name)
        unique_cities.update([city_name])
        for character in city_name:
            valid_characters.update([character])
        country_name = countries[country_code]['name']
        for character in country_name:
            valid_characters.update([character])

lines: List[str] = []  # 650 lines

all_characters: Set[str] = set()

with text_file.open(encoding="utf8") as file_handler:
    for line in file_handler.readlines():
        modified_line = line.rstrip('\n')
        lines.append(modified_line)
        for character in modified_line:
            all_characters.update([character])

nonvalid_characters: Set[str] = all_characters - valid_characters
# Create translation table
nonvalid_translation: str = "".join(list(nonvalid_characters))
translation_table = dict.fromkeys(map(ord, nonvalid_translation), None)


def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("utf-8")


def get_search_terms(current_line: str) -> Dict[int, Set[str]]:
    # Remove unwanted characters
    modified_line = current_line.translate(translation_table)
    # Remove multiple spaces
    modified_line = re.sub(r"\s\s+", " ", modified_line)
    words = [word.rstrip(",") for word in modified_line.split(" ")]

    results: Dict[int, Set[str]] = {}
    for partition in partitions(words):
        for subpartition in partition:
            subpartition_word_count: int = len(subpartition)
            if subpartition_word_count not in results.keys():
                results[subpartition_word_count] = set()
            result = " ".join(subpartition)
            results[subpartition_word_count].update([result])
    return results


# Data-frame data
df_data: List[List[str]] = []

for line in lines:
    search_terms: Dict[int, Set[str]] = get_search_terms(line)

    # Create a dictionary with cities as keys and country codes as values
    found_cities: Dict[str, str] = {}
    found_countries: Set[str] = set()

    for search_term_length, search_term in search_terms.items():
        if search_term_length in sorted(group_cities_by_word_count.keys()):
            # Create a dictionary with normalized cities as keys and country codes as values
            cities_and_countries: Dict[str, str] = {normalize_text(current[:-3]): current[-2:] for current in
                                                    group_cities_by_word_count[search_term_length]}
            # Create a set of normalized cities from previous dictionary
            subgroup_cities_by_word_count: Set[str] = set(
                [normalize_text(city_key) for city_key in cities_and_countries.keys()])
            # Compare original search term with normalized cities
            intersections: Set[str] = search_term.intersection(subgroup_cities_by_word_count)
            if len(intersections) > 0:
                longest_word = max(list(intersections), key=len)
                country_iso = cities_and_countries[longest_word]
                # Compare original search term with non normalized cities
                original_city = [current[:-3] for current in group_cities_by_word_count[search_term_length] if
                                 normalize_text(current[:-3]) == longest_word][0]
                found_cities[original_city] = countries[country_iso]['name']
        if search_term_length in group_countries_by_word_count.keys():
            subgroup_countries_by_word_count: Set[str] = set(group_countries_by_word_count[search_term_length])
            intersections: Set[str] = search_term.intersection(subgroup_countries_by_word_count)
            if len(intersections) > 0:
                found_countries.update(intersections)

    # Remove duplicate countries
    longest_word = ""
    if len(found_cities) > 0:
        longest_word = max(found_cities.keys(), key=len)
    if longest_word in found_cities:
        found_countries.clear()
        # Add country
        found_countries.add(found_cities[longest_word])

    df_data.append([line, ", ".join(list(found_countries)), longest_word])

# Create Panda's dataframe
column_names = ['headline', 'countries', 'cities']
live_project_df = pd.DataFrame(df_data, columns=column_names)

# Export to CSV
live_project_df.to_csv("./data/clean.csv", index=False, quoting=csv.QUOTE_ALL)
