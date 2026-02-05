# Final Transformation & Feature Engineering

This domain is dedicated to working on the **unified, clean, and enriched** dataset. It is the final layer before the data is handed over to the search engine indexer.

## What we do
We perform high-level preparation tasks to make the data "search-ready":

- **Metadata Enrichment**: Adding fixed metadata like `country_code` and `country_name`.
- **Feature Engineering**: Creating calculated columns for search and display.
    - `display_address`: A comma-separated string for user-friendly display.
    - `merged_address`: A space-separated string containing all address components, used for "search as you type" functionality.
- **Data Normalization**:
    - **Flag Casting**: Converting all boolean flags to `Int8` for compatibility.
    - **Redundancy Removal**: Nulling the `name` field for street records (where the name is already in the `street` field).

## Why it's important
- **Consistency**: Ensures that regardless of the source (city, street, or address), the user sees a consistent presentation.
- **Search Performance**: Pre-calculating search fields reduces complexity at query time. The `merged_address` column is specifically designed to power efficient prefix-based searching.
- **User Experience**: Fine-tuning how information is displayed to the user.

## Module: `features.py`
This module contains functions that operate on the final Polars DataFrame to add or modify columns for search and display purposes.

- `add_country_columns`: Adds `country_code` (DE) and `country_name` (Germany).
- `add_display_address`: Creates the `display_address` column for UI display.
- `add_merged_address`: Creates the `merged_address` column for the "search as you type" feature.
- `add_is_full_address`: Adds a flag indicating if all core address components are present.
- `cast_is_flags_to_int`: Casts `is_city`, `is_street`, `is_place`, and `is_full_address` to `Int8`.
- `null_name_for_streets`: Sets the `name` field to `None` for street records to avoid display redundancy.
