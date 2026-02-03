# Address Cleaning

We clean address data to ensure all records in the search engine are geographically located.

## What we clean
- **Geospatial**: We remove all rows that do not have valid **latitude and longitude**.
- **Meaningless Entries**: We remove entries that have coordinates but no other useful data (no name, street, house number, etc.).

## Normalization
- **House Number Lists**: We split entries where multiple house numbers are listed (e.g., `1;3;5`) into separate records.
- **House Number Ranges**: We expand ranges (e.g., `106-108` or `16a-16e`) into individual address entries.
- **House Number Length**: We remove (nullify) house numbers that exceed 30 characters to filter out data noise.
- **Postal Code Length**: We remove (nullify) postal codes that are not exactly 5 digits long (typical for Germany) to ensure data consistency.

## Enrichment
- **is_place**: We add a boolean flag `is_place` for all entries that have a valid `name`.

## Why it's important
- **Geocoding Integrity**: Addresses without coordinates cannot be placed on a map.
- **Search Relevance**: Entries without any descriptive fields (like street or house number) are noise.
- **Search Granularity**: Splitting lists and ranges ensures that every single house number is individually searchable and discoverable.
- **Data Quality**: Removing excessively long house numbers or invalid postal codes filters out corrupted or incorrect data.
- **Improved UX**: The `is_place` flag helps distinguish between generic addresses and specific named locations.
