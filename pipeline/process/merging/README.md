# Dataset Merging

This domain handles the consolidation of cleaned cities, streets, and addresses into a unified dataset for indexing.

## What we do
We transform and align different data sources (cities, streets, addresses) into a common schema.

### Merging Rules
- **Unified Schema**: Every entry is assigned a `uid` and aligned to a standard set of columns (`name`, `street`, `housenumber`, `postcode`, `city`, `lat`, `lon`).
- **Source Tracking**: We preserve the origin using `source_type` and `source_id`.
- **Feature Flags**: We maintain integer flags (`is_city`, `is_street`, `is_place`) as `Int8` (0 or 1) to allow for flexible filtering and ranking during search.
- **Street Alignment**: For street records, the `name` column is aligned with the `street` column during the merge to ensure consistent identification.

## Why it's important
- **Search Efficiency**: A single, flat dataset is much faster to index and query than multiple disparate tables.
- **Consistency**: Normalizing all entries to the same schema ensures that the search engine can handle different result types uniformly.
- **Categorization**: The unified integer flags allow the frontend and search engine to easily distinguish between a city, a street, or a specific point of interest using standard numeric comparisons.
