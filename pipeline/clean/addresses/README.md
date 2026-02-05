# Address Cleaning

We clean address data to ensure all records in the search engine are geographically located and correctly formatted.

---

## Cleaning Functions (Chronological Order)

The cleaning process follows this sequence:

### 1. [clean_addresses_geo](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L3-L10)
Removes all rows that do not have valid **latitude and longitude**.

### 2. [clean_addresses_geo_and_content](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L13-L27)
Removes entries that have coordinates but no other meaningful data (no name, street, house number, postcode, or city).

### 3. [add_is_place](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L30-L36)
Adds a boolean flag `is_place`.
- **Return Value**: `1` if a valid `name` exists, `0` otherwise.

### 4. [explode_housenumber_lists](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L38-L65)
Splits entries where multiple house numbers are listed (e.g., `1;3;5`) into separate records.

### 5. [expand_housenumber_ranges_df](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L100-L116)
Expands ranges (e.g., `106-108` or `16a-16e`) into individual address entries.

### 6. [nullify_too_long_housenumbers](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L122-L131)
Nullifies house numbers that exceed 20 characters to filter out noise.

### 7. [nullify_long_postcodes](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L134-L143)
Nullifies postal codes that are 6 characters or longer.

### 8. [nullify_short_postcodes](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/clean/addresses/clean_addresses.py#L145-L154)
Nullifies postal codes that are 4 characters or shorter.

---

## Why it's important

- **Geocoding Integrity**: Addresses without coordinates cannot be placed on a map.
- **Search Relevance**: Entries without any descriptive fields are noise.
- **Search Granularity**: Splitting lists and ranges ensures that every house number is individually searchable.
- **Data Quality**: Filtering invalid postal codes and long house numbers ensures consistency.
