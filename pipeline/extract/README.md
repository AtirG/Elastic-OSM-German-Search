# OSM Extraction – Germany

## Goal
Extract cities and streets from the Germany OpenStreetMap `.pbf` file and convert the graph-based OSM data into row-based CSV files. This stage is designed to be **simple and fast**, providing a foundational dataset for subsequent indexing.

> **Note:** Accuracy improvements (postcodes, polygons, enrichment) are handled in later pipeline stages.

---

## Data Pipeline Overview

The extraction follows a two-pass approach to transform spatial nodes and ways into a flat, searchable format.



### 1. City Extraction
* **Source:** OSM Node elements.
* **Filter:** `place` IN (`city`, `town`, `village`).
* **Data:** Captures coordinates and stores all supplementary tags as JSON.

### 2. Street Extraction
* **Source:** OSM Way elements with a `highway` tag.
* **Geometry:** Computes a simple centroid from associated way nodes.
* **Association:** Assigns each street to the **nearest city** using a **KD-Tree** for spatial lookup.

---

## Technical Specifications

### Input
* `germany-latest.osm.pbf` (Standard OSM extract)

### Output Files
| File | Columns                                                                |
| :--- |:-----------------------------------------------------------------------|
| `cities.csv` | `id`, `name`, `place`, `lat`, `lon`, `other_tags`                      |
| `streets.csv` | `id`, `name`, `highway`, `lat`, `lon`, `city_id`, `other_tags` |

*Files are generated locally and are not committed to version control.*

### Why KD-Tree?
* **Performance:** Offers $O(\log n)$ lookup speeds.
* **Scalability:** Efficiently handles the millions of street segments found in the Germany extract.
* **Purpose:** Sufficient for search bootstrapping; exact administrative boundary matching is deferred to the polygon enrichment stage.

---

## Trade-offs & Limitations
* **Spatial Accuracy:** Streets are linked by proximity (nearest city), not by administrative polygon intersection.
* **Data Completeness:** Some streets may lack names; postal codes are not processed in this step.
* **Optimization:** These limitations are intentional to keep the extraction runtime minimal.

---

## Usage

```bash
python extract_osm.py path/to/germany-latest.osm.pbf