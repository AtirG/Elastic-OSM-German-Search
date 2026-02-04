# Infrastructure & Services

This directory contains the configurations for running the necessary services using Docker.

## Elasticsearch

The search engine is powered by Elasticsearch. We use a single-node configuration for development.

### Deployment

To start the Elasticsearch container:

```bash
cd docker/elasticsearch
docker compose up -d
```

### Configuration
- **Image**: `elasticsearch:8.15.0`
- **Port**: `9200` (Mapping: `9200:9200`)
- **Security**: Disabled for local development (`xpack.security.enabled=false`)
- **Persistence**: Data is stored in the Docker volume `es_data`.
- **Custom Config**: `./elasticsearch.yml` is mounted to the container.

### Health Check

You can verify that Elasticsearch is running by visiting:
[http://localhost:9200](http://localhost:9200)

Or using curl:
```bash
curl http://localhost:9200
```
