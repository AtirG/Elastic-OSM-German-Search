# City Cleaning

We clean city data to ensure high-quality search results for the OSM Germany address search.

---

## Cleaning Functions (Chronological Order)

### 1. [clean_cities](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/cities/clean_cities.py#L3-L23)
Removes all rows that do not have a valid name, latitude, and longitude.

### 2. [add_is_city](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/cities/clean_cities.py#L25-L28)
Adds a boolean flag `is_city`.
- **Return Value**: `1` for all valid city entries.

---

## Why it's important

- **Search Relevance**: Cities without names are useless for text search.
- **Geospatial Integrity**: Cities without coordinates cannot be mapped or used for spatial enrichment.
