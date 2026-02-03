# Postcode Geo-Enrichment

This domain handles the spatial enrichment of postcodes for entries that are missing them in OSM.

## Workflow

The enrichment process follows a 4-step workflow after the initial merge:

1. **Export Missing**: Use `export_for_postcode_enrichment` to extract all rows lacking a postcode into a minimal CSV.
2. **Spatial Join**: Use `enrich_postcodes_from_polygons` to perform a point-in-polygon lookup against Germany's PLZ (Postleitzahl) polygons.
3. **Re-Merge**: Use `merge_postcode_enrichment` to join the newly found postcodes back into the main dataset.
4. **Final Cleanup**: Use `drop_rows_without_postcode` to remove any remaining entries that still lack a postcode (typically because they fall outside the geographic boundaries of Germany).

## Why it's important
- **Search Quality**: Users often search by postcode. OSM data is frequently incomplete for street and address nodes.
- **Data Integrity**: Validating postcodes against geographic polygons ensures high accuracy and removes coordinate noise from outside the target area.
- **Completeness**: By backfilling postcodes via spatial lookups, we ensure the search engine provides a consistent experience across all entry types (cities, streets, and individual buildings).
