import geopandas as gpd
import pandas as pd
import polars as pl
import string

def export_for_postcode_enrichment(
    merged_dataset: pl.DataFrame,
    output_path: str = "data/processed/merged_for_postcode_enrichment.csv",
):
    """
    Export minimal data needed for postcode geo-enrichment (rows without postcodes).
    """
    (
        merged_dataset
        .filter(pl.col("postcode").is_null() | (pl.col("postcode") == ""))
        .select([
            "uid",
            "lat",
            "lon",
            "postcode",
        ])
        .write_csv(output_path)
    )

def enrich_postcodes_from_polygons(
    input_csv: str,
    postcode_geojson: str,
    output_csv: str,
    chunk_size: int = 50_000,
):
    """
    Adds postcode_enriched to a CSV using point-in-polygon against PLZ GeoJSON.
    """

    postcodes = gpd.read_file(postcode_geojson)[["plz", "geometry"]]
    postcodes.crs = "EPSG:4326"
    postcodes.geometry = postcodes.geometry.simplify(tolerance=0.0001)

    first_write = True
    processed = 0

    for chunk in pd.read_csv(input_csv, chunksize=chunk_size):
        gdf = gpd.GeoDataFrame(
            chunk,
            geometry=gpd.points_from_xy(chunk.lon, chunk.lat),
            crs="EPSG:4326"
        )

        joined = gpd.sjoin(
            gdf,
            postcodes,
            how="left",
            predicate="within"
        )

        output = (
            joined
            .rename(columns={"plz": "postcode_enriched"})
            .drop(columns=["geometry", "index_right"])
        )

        output.to_csv(
            output_csv,
            mode="w" if first_write else "a",
            index=False,
            header=first_write
        )

        processed += len(chunk)
        print(f"✅ Processed {processed:,} rows")
        first_write = False

    print("🎉 Postcode enrichment complete:", output_csv)


def merge_postcode_enrichment(
    merged: pl.DataFrame,
    enriched: pl.DataFrame,
) -> pl.DataFrame:
    """
    Merge the enriched postcodes back into the main dataset.
    """
    return (
        merged
        .join(enriched, on="uid", how="left")
        .with_columns(
            pl.when(
                pl.col("postcode").is_null()
                & pl.col("postcode_enriched").is_not_null()
            )
            .then(pl.col("postcode_enriched"))
            .otherwise(pl.col("postcode"))
            .alias("postcode")
        )
        .drop("postcode_enriched")
    )


def drop_rows_without_postcode(df: pl.DataFrame) -> pl.DataFrame:
    """
    Remove rows that still don't have a postcode (likely outside Germany or invalid).
    """
    return df.filter(
        pl.col("postcode").is_not_null()
        & (pl.col("postcode") != "")
    )
