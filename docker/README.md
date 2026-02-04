# Infrastructure & Services

This directory contains the configurations for running the necessary services using Docker.

## Elasticsearch

The search engine is powered by Elasticsearch. We use a single-node configuration for development.

## Deployment

The search infrastructure is managed via the root-level `docker-compose.yml`. Follow these steps for a clean deployment:

### 1. Start Elasticsearch
```bash
docker compose up -d elasticsearch
```
Wait for the service to start. Verify at [http://localhost:9200](http://localhost:9200).

### 2. Initialize Index Schema
Run the initialization container to create indices and aliases:
```bash
docker compose up es_init
```
**Verification Commands:**
- Indices: `curl "http://localhost:9200/_cat/indices?v"`
- Aliases: `curl "http://localhost:9200/_cat/aliases?v"`
- Mappings: `curl "http://localhost:9200/osm_addresses_de_v1/_mapping?pretty"`

### 3. Start Logstash Ingestion
Ensure your `data/processed/final_addresses.csv` is correctly prepared, then:
```bash
docker compose up -d logstash
```
**Monitor Ingestion Progress:**
```bash
curl "http://localhost:9200/osm_addresses_global/_count"
```
The ingestion typically takes ~30 minutes for the full Germany dataset.

### Health Check

You can verify that Elasticsearch is running by visiting:
[http://localhost:9200](http://localhost:9200)

Or using curl:
```bash
curl http://localhost:9200
```
