# Street Cleaning

We clean street data to ensure consistency and completeness for the OSM Germany address search.

## What we clean
We remove all rows that do not have a valid **combination of name, latitude, and longitude**.

## Enrichment
- **is_street**: We add a boolean flag `is_street` set to `True` for all valid street entries.

## Why it's important
- **Search Quality**: Streets without names cannot be searched or indexed effectively.
- **Spatial Accuracy**: Latitude and longitude are essential for identifying the street's location.
- **Classification**: The `is_street` flag allows the search engine to prioritize or filter for street-specific results.
