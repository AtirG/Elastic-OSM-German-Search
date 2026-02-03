# OSM Germany Address Search

This project extracts and processes OSM data for address searching in Germany.

## Pipeline Workflow

### Phase 1: Extraction
Extract data from OSM PBF files into raw CSVs.
```bash
python pipeline/extract/01_extract_osm.py data/germany-latest.osm.pbf
python pipeline/extract/02_extract_places_buildings.py data/germany-latest.osm.pbf
```
- **Output**: `cities.csv`, `streets.csv`, `addresses.csv`

### Phase 2: Cleaning
Clean and normalize each domain separately.
- **Cities**: Filter invalid names/coords, normalize characters.
- **Streets**: Filter invalid names/coords.
- **Addresses**: Filter invalid coords, split house number lists/ranges, validate postal codes.

### Phase 3: Merging & Processing
Consolidate the cleaned domains into a unified dataset for indexing.
- **Process**: Align all sources to a common schema.
- **Enrichment**: Add classification flags (`is_city`, `is_street`, `is_place`).

### Phase 4: Geo-Enrichment (Postcodes)
Backfill missing postcodes using spatial lookups.
- **Process**: Export rows without postcodes, perform point-in-polygon joins with PLZ polygons, and re-merge.
- **Cleanup**: Remove any remaining entries outside valid postcode boundaries.

### Phase 5: Feature Engineering & Final Prep
Prepare the consolidated dataset for indexing and display.
- **Process**: Add display columns, consolidate search fields, and apply final business rules.

---

## Directory Structure
- `pipeline/clean/`: Domain-specific cleaning logic ([Cities](pipeline/clean/cities/), [Streets](pipeline/clean/streets/), [Addresses](pipeline/clean/addresses/)).
- `pipeline/process/`: Data loading and preparation.
    - [Merging](pipeline/process/merging/): Unified dataset building.
    - [Enrichment](pipeline/process/enrichment/): Spatial postcode backfilling.
    - [Final](pipeline/process/final/): Feature engineering and display formatting.

