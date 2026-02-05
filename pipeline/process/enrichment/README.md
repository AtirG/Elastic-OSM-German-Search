# Spatial Enrichment

This domain handles the spatial enrichment of postcodes and administrative boundaries for entries using geographic polygons.

## Postcode Enrichment Workflow

The postcode enrichment process follows a 4-step workflow:

1. **Export Missing**: Use `export_for_postcode_enrichment` to extract rows lacking a postcode.
2. **Spatial Join**: Use `enrich_postcodes_from_polygons` to perform a point-in-polygon lookup against Germany's PLZ polygons.
3. **Re-Merge**: Use `merge_postcode_enrichment` to join the newly found postcodes back into the dataset.
4. **Final Cleanup**: Use `drop_rows_without_postcode` to remove entries that still lack a postcode.

## Admin Boundaries Enrichment Workflow

After postcode enrichment, we enrich the dataset with administrative names (Federal State, District, Municipality):

1. **Export for Admin**: Use `export_for_admin_enrichment` to extract `uid`, `lat`, and `lon` for all valid coordinates.
2. **Spatial Pivot**: Use `enrich_admin_levels_from_polygons` to look up administrative boundaries (Levels 4, 6, and 8) and pivot them into columns:
    - `admin4_name`: Federal State (Bundesland)
    - `admin6_name`: District (Regierungsbezirk / Kreis)
    - `admin8_name`: Municipality (Gemeinde)
3. **Re-Merge Admin**: Use `merge_admin_enrichment` to join these administrative names back into the main dataset.

## Why it's important
- **Search Quality**: Users often search by postcode or region (e.g., searching for a street in a specific Bundesland).
- **Data Integrity**: Validating postcodes and admin levels against geographic polygons ensures high accuracy.
- **Completeness**: Ensures the search engine can filter or rank results based on administrative hierarchy.
