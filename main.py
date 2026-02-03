import sys
import os

def main():
    print("OSM Germany Address Search Project")
    print("-" * 30)
    print("Project initialized and dependencies installed.")
    print("\nTo start the data extraction, run:")
    print("python pipeline/extract/01_extract_osm.py data/germany-latest.osm.pbf")
    
    # Check if data directory exists
    if not os.path.exists("data"):
        print("\nWarning: 'data' directory not found. Please ensure your OSM data is in the 'data' folder.")

if __name__ == "__main__":
    main()
