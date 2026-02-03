# Final Transformation & Feature Engineering

This domain is dedicated to working on the **unified, clean, and enriched** dataset. It is the final layer before the data is handed over to the search engine indexer.

## What we do
We perform high-level preparation tasks to make the data "search-ready":

- **Metadata Enrichment**: Adding fixed metadata like `country_code` and `country_name`.
- **Feature Engineering**: Creating calculated columns for search and display.
- **Final Filtering**: Last-minute data validation.

## Why it's important
- **Consistency**: Ensures that regardless of the source (city, street, or address), the user sees a consistent presentation.
- **Search Performance**: Pre-calculating search fields reduces complexity at query time.
- **User Experience**: Fine-tuning how information is displayed to the user.

## Module: `features.py`
This module contains functions that operate on the final Polars DataFrame to add or modify columns for search and display purposes.
