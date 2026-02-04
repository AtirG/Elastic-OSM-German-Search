# Logstash Ingestion Pipeline

This directory contains the Logstash configuration used to ingest the processed OSM address data into Elasticsearch.

## Pipeline Configuration
- **Location**: `pipeline/logstash.conf`
- **Input**: Reads from `/data/final_addresses.csv` (mapped from the root `data/processed/final_addresses.csv` via Docker Compose).
- **Filter**: Handles CSV parsing, data type conversion, and preparation for Elasticsearch.
- **Output**: Sends data to the `elasticsearch` service on port `9200`.

## Usage
The Logstash service is started as part of the main `docker-compose.yml` at the project root.

```bash
docker compose up -d
```

Ensure that the data pipeline has been run and the `data/processed/final_addresses.csv` file exists before starting Logstash, as it depends on this file for ingestion.
