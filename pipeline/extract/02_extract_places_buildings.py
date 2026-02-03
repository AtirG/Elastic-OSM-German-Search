import osmium
import csv
import sys
import os

BATCH_SIZE = 100000

class AddressHandler(osmium.SimpleHandler):
    def __init__(self, writer):
        super().__init__()
        self.writer = writer
        self.count = 0

    def node(self, n):
        # Extract address nodes
        if 'addr:housenumber' not in n.tags:
            return

        self.writer.writerow({
            "id": n.id,
            "name": n.tags.get("name", ""),
            "building": "",
            "housenumber": n.tags.get("addr:housenumber", ""),
            "street": n.tags.get("addr:street", ""),
            "postcode": n.tags.get("addr:postcode", ""),
            "city": n.tags.get("addr:city", ""),
            "lat": n.location.lat,
            "lon": n.location.lon
        })

        self.count += 1
        if self.count % BATCH_SIZE == 0:
            print(f"Processed {self.count:,} addresses...")

    def way(self, w):
        # Extract buildings
        if 'building' not in w.tags:
            return

        try:
            coords = [(n.lat, n.lon) for n in w.nodes if n.location.valid()]
        except (osmium.InvalidLocationError, Exception):
            return

        if not coords:
            return

        centroid_lat = sum(lat for lat, lon in coords) / len(coords)
        centroid_lon = sum(lon for lat, lon in coords) / len(coords)

        self.writer.writerow({
            "id": w.id,
            "name": w.tags.get("name", ""),
            "building": w.tags.get("building", ""),
            "housenumber": w.tags.get("addr:housenumber", ""),
            "street": w.tags.get("addr:street", ""),
            "postcode": w.tags.get("addr:postcode", ""),
            "city": w.tags.get("addr:city", ""),
            "lat": centroid_lat,
            "lon": centroid_lon
        })

        self.count += 1
        if self.count % BATCH_SIZE == 0:
            print(f"Processed {self.count:,} addresses...")

def main(pbf_path):
    output_path = "data/raw/addresses.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Extracting buildings and address nodes from {pbf_path}...")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "building", "housenumber", "street", "postcode", "city", "lat", "lon"
        ])
        writer.writeheader()

        handler = AddressHandler(writer)
        handler.apply_file(pbf_path, locations=True)

    print(f"✔ Done — wrote {handler.count:,} total records to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline/extract/02_extract_places_buildings.py <path_to_osm.pbf>")
        sys.exit(1)
    main(sys.argv[1])
