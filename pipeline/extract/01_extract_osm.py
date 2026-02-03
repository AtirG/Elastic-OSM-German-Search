import osmium
import csv
import json
import sys
from scipy.spatial import cKDTree

PLACE_TYPES = {"city", "town", "village"}
BATCH_SIZE = 50000

class CityHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.cities = []

    def node(self, n):
        place = n.tags.get("place")
        if place in PLACE_TYPES and n.location.valid():
            tags = dict(n.tags)
            tags.pop("place", None)
            self.cities.append({
                "id": n.id,
                "name": n.tags.get("name", ""),
                "place": place,
                "lat": n.location.lat,
                "lon": n.location.lon,
                "other_tags": json.dumps(tags, ensure_ascii=False)
            })

class StreetHandler(osmium.SimpleHandler):
    def __init__(self, kd_tree, city_ids, writer):
        super().__init__()
        self.kd_tree = kd_tree
        self.city_ids = city_ids
        self.writer = writer
        self.count = 0

    def way(self, w):
        if "highway" not in w.tags:
            return

        coords = [(n.lat, n.lon) for n in w.nodes if n.location.valid()]
        if not coords:
            return

        centroid_lat = sum(lat for lat, lon in coords) / len(coords)
        centroid_lon = sum(lon for lat, lon in coords) / len(coords)
        _, idx = self.kd_tree.query((centroid_lat, centroid_lon))
        city_id = self.city_ids[idx]

        tags = dict(w.tags)
        highway = tags.pop("highway")
        name = tags.pop("name", "")
        self.writer.writerow({
            "id": w.id,
            "name": name,
            "highway": highway,
            "lat": centroid_lat,
            "lon": centroid_lon,
            "city_id": city_id,

        })

        self.count += 1
        if self.count % BATCH_SIZE == 0:
            print(f"Processed {self.count:,} streets…")

def main(pbf_path):
    # === PASS 1: Extract places ===
    print("Extracting place nodes…")
    city_handler = CityHandler()
    city_handler.apply_file(pbf_path, locations=True)
    cities = city_handler.cities
    print(f"→ Found {len(cities):,} place nodes.")

    with open("data/raw/cities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id","name","place","lat","lon","other_tags"])
        writer.writeheader()
        writer.writerows(cities)

    coords = [(c["lat"], c["lon"]) for c in cities]
    city_ids = [c["id"] for c in cities]
    kd_tree = cKDTree(coords)

    # === PASS 2: Extract streets ===
    print("Extracting highway ways…")
    with open("data/raw/streets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id","name","highway","lat","lon","city_id","other_tags"]
        )
        writer.writeheader()

        street_handler = StreetHandler(kd_tree, city_ids, writer)
        street_handler.apply_file(pbf_path, locations=True)

    print(f"✔ Done — wrote {street_handler.count:,} streets to streets.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_germany_osm.py <path_to_germany-latest.osm.pbf>")
        sys.exit(1)
    main(sys.argv[1])