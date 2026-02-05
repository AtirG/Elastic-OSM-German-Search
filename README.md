# OSM Germany Address Search

This project extracts and processes OpenStreetMap (OSM) data to build a high-performance address search engine for Germany.

---

## Data Pipeline Workflow (Chronological)

The pipeline is executed in a strict sequential order to transform raw OSM data into an enriched, searchable dataset.

### 1. Extraction
Extract raw data from the German OSM PBF file.
- **Scripts**: `01_extract_osm.py`, `02_extract_places_buildings.py`, `03_extract_cities_boundries.py`.
- **Outputs**: `cities.csv`, `streets.csv`, `addresses.csv`.

### 2. Cleaning & Normalization
Perform domain-specific cleaning using Polars.
- **Order**: [Addresses](pipeline/clean/addresses/) → [Cities](pipeline/clean/cities/) → [Streets](pipeline/clean/streets/).
- **Key Tasks**: Splitting house number ranges, filtering invalid coordinates, and adding boolean flags (`is_place`, `is_city`, `is_street`) as `1` or `0`.

### 3. Merging
Consolidate the cleaned domains into a single unified dataset.
- **Script**: [merged_dataset.py](pipeline/process/merging/merged_dataset.py).
- **Goal**: Align all sources to a common schema with a unique `uid`.

### 4. Spatial Enrichment
Backfill missing postcodes and add administrative boundaries using geographic polygons.
- **Module**: [postcode_enrichment.py](pipeline/process/enrichment/postcode_enrichment.py).
- **Enrichment**: Federal State (Admin 4), District (Admin 6), and Municipality (Admin 8).

### 5. Final Feature Engineering
Prepare the data for the search index.
- **Module**: [features.py](pipeline/process/final/features.py).
- **Key Features**: `display_address` for UI, `merged_address` for "search as you type", and the `is_full_address` (1/0) flag.

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

