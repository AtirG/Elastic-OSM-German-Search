# City Cleaning

We clean city data to ensure high-quality search results for the OSM Germany address search.

## What we clean
We remove all rows that do not have a valid **combination of name, latitude, and longitude**.

## Why it's important
- **Search Relevance**: Cities without names are useless for text search.
- **Geospatial Integrity**: Cities without coordinates cannot be mapped or used for spatial enrichment.

## Enrichment
- **is_city**: We add a boolean flag `is_city` set to `True` for all valid city entries.
- **Postal Codes**: We will be adding postal codes using Germany's postal code polygons to enrich city data.
