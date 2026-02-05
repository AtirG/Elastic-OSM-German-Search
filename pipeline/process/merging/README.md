# Dataset Merging

This domain handles the consolidation of cleaned cities, streets, and addresses into a unified dataset for indexing.

---

## Merging Functions (Chronological Order)

### 1. [build_merged_dataset](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/process/merging/merged_dataset.py#L3-L66)
Consolidates cities, streets, and addresses into a single Polars DataFrame.
- **Normalization**: Aligns all sources to a unified schema (`uid`, `source_type`, `source_id`, `name`, `street`, `housenumber`, `postcode`, `city`, `lat`, `lon`).
- **Return Values (Boolean Flags)**:
    - `is_city`: `1` for city records, `0` otherwise.
    - `is_street`: `1` for street records, `0` otherwise.
    - `is_place`: `1` for address records, `0` otherwise.

---

## Why it's important

- **Search Efficiency**: A single, flat dataset is much faster to index and query than multiple disparate tables.
- **Consistency**: Normalizing all entries to the same schema ensures that the search engine can handle different result types uniformly.
- **Categorization**: Unified integer flags allow the frontend and search engine to easily distinguish between result types using numeric comparisons.
