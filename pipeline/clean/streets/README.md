# Street Cleaning

We clean street data to ensure consistency and completeness for the OSM Germany address search.

---

## Cleaning Functions (Chronological Order)

### 1. [clean_streets](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/streets/clean_streets.py#L3-L23)
Removes all rows that do not have a valid combination of name, latitude, and longitude.

### 2. [add_is_street](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/streets/clean_streets.py#L26-L29)
Adds a boolean flag `is_street`.
- **Return Value**: `1` for all valid street entries.

---

## Why it's important

- **Search Quality**: Streets without names cannot be searched or indexed effectively.
- **Spatial Accuracy**: Latitude and longitude are essential for identifying the street's location.
- **Classification**: The `is_street` flag allows the search engine to prioritize or filter for street-specific results.
