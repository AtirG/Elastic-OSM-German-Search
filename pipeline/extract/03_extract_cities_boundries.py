import osmium
import geopandas as gpd
from shapely.geometry import shape
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PBF = BASE_DIR / "data" / "germany-latest.osm.pbf"
OUTPUT_DIR = BASE_DIR / "data" / "cities_boundaries"
OUTPUT_FILE = OUTPUT_DIR / "cities_boundaries.geojson"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class AdminBoundaryHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.factory = osmium.geom.GeoJSONFactory()
        self.records = []

    def area(self, a):
        tags = a.tags

        if tags.get("boundary") != "administrative":
            return

        admin_level = tags.get("admin_level")
        if admin_level not in {"2", "4", "6", "8"}:
            return

        try:
            geojson = self.factory.create_multipolygon(a)
            geom = shape(json.loads(geojson))

            self.records.append({
                "osm_id": a.id,
                "name": tags.get("name"),
                "admin_level": admin_level,
                "geometry": geom,
            })
        except Exception:
            pass


def main():
    handler = AdminBoundaryHandler()
    handler.apply_file(INPUT_PBF, locations=True)

    if not handler.records:
        raise RuntimeError("No administrative boundaries extracted")

    gdf = gpd.GeoDataFrame(
        handler.records,
        geometry="geometry",
        crs="EPSG:4326"
    )

    gdf.to_file(OUTPUT_FILE, driver="GeoJSON")
    print(f"✅ written {len(gdf)} admin boundaries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
