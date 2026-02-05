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

def export_for_admin_enrichment(
    merged_dataset: pl.DataFrame,
    output_path: str = "data/processed/merged_for_admin_enrichment.csv",
):
    (
        merged_dataset
        .select([
            "uid",
            "lat",
            "lon",
        ])
        .filter(
            pl.col("lat").is_not_null()
            & pl.col("lon").is_not_null()
        )
        .write_csv(output_path)
    )

    def enrich_admin_levels_from_polygons(
            input_csv: str,
            admin_geojson: str,
            output_csv: str,
            chunk_size: int = 50_000,
    ):
        admins = gpd.read_file(admin_geojson)[
            ["admin_level", "name", "geometry"]
        ]
        admins = admins[admins["admin_level"].isin(["4", "6", "8"])]
        admins.crs = "EPSG:4326"

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
                admins,
                how="left",
                predicate="within"
            )

            pivoted = (
                joined
                .pivot_table(
                    index="uid",
                    columns="admin_level",
                    values="name",
                    aggfunc="first"
                )
                .reset_index()
                .rename(columns={
                    "4": "admin4_name",
                    "6": "admin6_name",
                    "8": "admin8_name",
                })
            )

            pivoted.to_csv(
                output_csv,
                mode="w" if first_write else "a",
                index=False,
                header=first_write
            )

            processed += len(chunk)
            print(f"✅ Processed {processed:,} rows")
            first_write = False

        print("🎉 Admin enrichment complete:", output_csv)

def enrich_admin_levels_from_polygons(
    input_csv: str,
    admin_geojson: str,
    output_csv: str,
    chunk_size: int = 50_000,
):
    admins = gpd.read_file(admin_geojson)[
        ["admin_level", "name", "geometry"]
    ]
    admins = admins[admins["admin_level"].isin(["4", "6", "8"])]
    admins.crs = "EPSG:4326"

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
            admins,
            how="left",
            predicate="within"
        )

        pivoted = (
            joined
            .pivot_table(
                index="uid",
                columns="admin_level",
                values="name",
                aggfunc="first"
            )
            .reset_index()
            .rename(columns={
                "4": "admin4_name",
                "6": "admin6_name",
                "8": "admin8_name",
            })
        )

        pivoted.to_csv(
            output_csv,
            mode="w" if first_write else "a",
            index=False,
            header=first_write
        )

        processed += len(chunk)
        print(f"✅ Processed {processed:,} rows")
        first_write = False

    print("🎉 Admin enrichment complete:", output_csv)

def merge_admin_enrichment(
        merged: pl.DataFrame,
        enriched: pl.DataFrame,
) -> pl.DataFrame:
    return merged.join(enriched, on="uid", how="left")


def enrich_geo_from_polygons(
    input_csv: str,
    postcode_geojson: str,
    admin_geojson: str,
    output_csv: str,
    chunk_size: int = 50_000,
):
    postcodes = gpd.read_file(postcode_geojson)[["plz", "geometry"]]
    postcodes.crs = "EPSG:4326"
    postcodes.geometry = postcodes.geometry.simplify(0.0001)

    admins = gpd.read_file(admin_geojson)[["admin_level", "name", "geometry"]]
    admins = admins[admins["admin_level"].isin(["4", "6", "8"])]
    admins.crs = "EPSG:4326"

    first_write = True
    processed = 0

    for chunk in pd.read_csv(input_csv, chunksize=chunk_size):
        gdf = gpd.GeoDataFrame(
            chunk,
            geometry=gpd.points_from_xy(chunk.lon, chunk.lat),
            crs="EPSG:4326",
        )

        # --- postcode ---
        gdf = gpd.sjoin(gdf, postcodes, how="left", predicate="within")
        gdf = gdf.drop(columns=["index_right"], errors="ignore")

        # --- admin ---
        gdf = gpd.sjoin(gdf, admins, how="left", predicate="within")
        gdf = gdf.drop(columns=["index_right"], errors="ignore")

        pivot_admin = (
            gdf
            .pivot_table(index="uid", columns="admin_level", values="name", aggfunc="first")
            .rename(columns={"4": "admin4_name", "6": "admin6_name", "8": "admin8_name"})
        )

        out = (
            gdf[["uid", "postcode", "plz"]]
            .drop_duplicates("uid")
            .rename(columns={"plz": "postcode_enriched"})
            .merge(pivot_admin, on="uid", how="left")
        )

        out.to_csv(
            output_csv,
            mode="w" if first_write else "a",
            index=False,
            header=first_write,
        )

        processed += len(chunk)
        print(f"✅ Processed {processed:,} rows")
        first_write = False

    print("🎉 Geo enrichment complete:", output_csv)


def export_for_geo_enrichment(
    merged: pl.DataFrame,
    output_path="data/processed/merged_for_geo_enrichment.csv",
):
    (
        merged
        .select(["uid", "lat", "lon", "postcode"])
        .filter(pl.col("lat").is_not_null() & pl.col("lon").is_not_null())
        .write_csv(output_path)
    )




enrich_geo_from_polygons(
    input_csv="data/processed/merged_for_geo_enrichment.csv",
    postcode_geojson="data/plz-5stellig-2023.geojson",
    admin_geojson="data/cities_boundaries/cities_boundaries.geojson",
    output_csv="data/processed/geo_enriched.csv",
)



def merge_geo_enrichment(m: pl.DataFrame, geo: pl.DataFrame) -> pl.DataFrame:
    return (
        m
        .join(geo, on="uid", how="left")
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


def merge_and_clean_postcode(m: pl.DataFrame) -> pl.DataFrame:
    return (
        m
        .with_columns(
            pl.when(pl.col("postcode").is_null())
              .then(pl.col("postcode_right"))
              .otherwise(pl.col("postcode"))
              .str.replace(r"\.0$", "")
              .alias("postcode")
        )
        .drop("postcode_right")
    )