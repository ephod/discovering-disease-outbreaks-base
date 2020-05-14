from typing_extensions import TypedDict


class City(TypedDict):
    geonameid: int  # Dictionary's key and unique ID
    name: str  # City's name
    latitude: float
    longitude: float
    countrycode: str  # Country's foreign key
    population: int
    timezone: str
    admin1code: str


class Country(TypedDict):
    geonameid: int  # Country's unique ID
    name: str  # Country's name
    iso: str  # Dictionary's key
    iso3: str
    isonumeric: int
    fips: str
    continentcode: str
    capital: str
    areakm2: int
    population: int
    tld: str
    currencycode: str
    currencyname: str
    phone: str
    postalcoderegex: str
    languages: str
    neighbours: str
