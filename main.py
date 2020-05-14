# Builtin Python modules
import itertools
import json
from pathlib import Path
from pprint import pprint
import re
import string
from typing import Dict, List, Set

from geonamescache import GeonamesCache

from helper import Cities, Countries

cities = Cities("./data/cities.json", GeonamesCache())
countries = Countries("./data/countries.json", GeonamesCache())

text_file: Path = Path('./data/headlines.txt')
assert text_file.is_file(), f"Wrong file: {text_file}"
