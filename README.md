# OSM Germany Address Search

This project extracts and processes OSM data for address searching in Germany.

## Data Pipeline Workflow

The build process follows a strict sequence to transform raw OSM data into a search-ready dataset.

### Step 1: Extraction
Extract 3 core files from the German OSM PBF into raw CSVs.
```bash
python pipeline/extract/01_extract_osm.py data/germany-latest.osm.pbf
python pipeline/extract/02_extract_places_buildings.py data/germany-latest.osm.pbf
```
- **Outputs**: `cities.csv`, `streets.csv`, `addresses.csv`.

### Step 2: Cleaning
Load the raw CSVs into Polars for high-performance cleaning and normalization.
Follow the cleaning instructions for each domain in this specific order:
1. **Addresses**: Normalize house numbers and filter invalid coordinates ([README](pipeline/clean/addresses/)).
2. **Cities**: Filter and normalize city names.
3. **Streets**: Clean street names and validate geometry.

### Step 3: Merging
Consolidate the three cleaned domains into a single, unified Polars DataFrame.
- **Location**: `pipeline/process/merging/`
- **Goal**: Align all sources to a common schema with a unique `uid`.

### Step 4: Postcode Geo-Enrichment
Fix rows missing postal codes using spatial lookups.
1. **Flat CSV Export**: Export the merged dataset to a CSV, dropping the geometry `location` column to keep it flat.
2. **Spatial Join**: Run `postcode_enrichment.py` to perform point-in-polygon joins with Germany's PLZ polygons.
3. **Re-Merge**: Re-import the enriched postcodes back into the main Polars pipeline.

### Step 5: Final Feature Engineering
Apply the final transformations in `pipeline/process/final/` to create the search-ready dataset.
This step adds the necessary columns for display and "search as you type" functionality.

**Final Dataset Schema:**
`uid, source_type, source_id, name, street, housenumber, postcode, city, lat, lon, is_city, is_street, is_place, country_code, country_name, display_address, is_full_address, merged_address`

---

## Infrastructure & Data Indexing

---

## Infrastructure & Data Indexing

The project uses Docker to manage the search infrastructure and data ingestion. The indexing process is performed in sequential steps.

### Step 1: Start Elasticsearch
Start only the Elasticsearch service and wait for it to become healthy.
```bash
docker compose up -d elasticsearch
```
**Verify Health:**
```bash
curl "http://localhost:9200"
```

### Step 2: Initialize Indices & Aliases
Once Elasticsearch is live, run the initialization service to create the required indices and aliases.
```bash
docker compose up es_init
```
**Verify Indices & Aliases:**
```bash
curl "http://localhost:9200/_cat/indices?v"
curl "http://localhost:9200/_cat/aliases?v"
```
Expect to see `osm_addresses_de_v1` and the alias `osm_addresses_global` pointing to it. You can also check mappings with:
```bash
curl "http://localhost:9200/osm_addresses_de_v1/_mapping?pretty"
```

### Step 3: Start Data Ingestion (Logstash)
Ensure `data/processed/final_addresses.csv` is ready, then start Logstash.
```bash
docker compose up -d logstash
```
The ingestion process takes approximately 30 minutes for the full German dataset.

**Monitor Progress:**
```bash
curl "http://localhost:9200/osm_addresses_global/_count"
```

---

## Directory Structure
- `pipeline/clean/`: Domain-specific cleaning logic ([Cities](pipeline/clean/cities/), [Streets](pipeline/clean/streets/), [Addresses](pipeline/clean/addresses/)).
- `pipeline/process/`: Data loading and preparation.
    - [Merging](pipeline/process/merging/): Unified dataset building.
    - [Enrichment](pipeline/process/enrichment/): Spatial postcode backfilling.
    - [Final](pipeline/process/final/): Feature engineering and display formatting.
- `es/`: Elasticsearch client and index management scripts.
- `logstash/`: Logstash pipeline configuration for indexing.
- `docker/`: Additional service-specific configurations.

