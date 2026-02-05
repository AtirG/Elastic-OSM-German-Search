# Spatial Enrichment

This domain handles the spatial enrichment of postcodes and administrative boundaries using geographic polygons.

---

## Combined Enrichment Workflow (Chronological Order)

For efficiency, we typically run the following sequence:

### 1. [export_for_geo_enrichment](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/process/enrichment/postcode_enrichment.py#L309-L318)
Exports a minimal CSV containing `uid`, `lat`, and `lon` for all entries requiring spatial lookup.

### 2. [enrich_geo_from_polygons](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/process/enrichment/postcode_enrichment.py#L249-L306)
Performs point-in-polygon lookups against both postcode (PLZ) and administrative boundaries.

### 3. [merge_geo_enrichment](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/process/enrichment/postcode_enrichment.py#L332-L346)
Joins the enriched postcodes and admin levels (4, 6, 8) back into the main dataset.

### 4. [merge_and_clean_postcode](file:///Users/atirgabay/PycharmProjects/osm-germany-address-search/pipeline/process/enrichment/postcode_enrichment.py#L349-L360)
Consolidates `postcode_enriched` with existing postcodes and ensures data consistency.

---

## Individual Workflows

The module also supports granular enrichment if needed:

- **Postcode Only**: `export_for_postcode_enrichment` → `enrich_postcodes_from_polygons` → `merge_postcode_enrichment` → `drop_rows_without_postcode`.
- **Admin Only**: `export_for_admin_enrichment` → `enrich_admin_levels_from_polygons` → `merge_admin_enrichment`.

---

## Why it's important

- **Search Quality**: Enables searching by postcode or specific administrative regions (Federal State, District, Municipality).
- **Data Integrity**: Validating postcodes and admin levels against geographic polygons ensures high accuracy.
- **Completeness**: Ensures every entry has its full geographic context.
