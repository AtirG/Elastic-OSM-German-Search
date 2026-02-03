import polars as pl

def build_merged_dataset(cities, streets, addresses):

    cities_norm = cities.select([
        pl.concat_str([pl.lit("city:"), pl.col("id")]).alias("uid"),
        pl.lit("city").alias("source_type"),
        pl.col("id").alias("source_id"),

        pl.col("name"),
        pl.lit(None, dtype=pl.Utf8).alias("street"),
        pl.lit(None, dtype=pl.Utf8).alias("housenumber"),
        pl.lit(None, dtype=pl.Utf8).alias("postcode"),
        pl.lit(None, dtype=pl.Utf8).alias("city"),
        pl.lit(None, dtype=pl.Int64).alias("city_id"),

        pl.col("lat"),
        pl.col("lon"),

        pl.col("is_city"),
        pl.lit(False).alias("is_street"),
        pl.lit(False).alias("is_place"),
    ])

    streets_norm = streets.select([
        pl.concat_str([pl.lit("street:"), pl.col("id")]).alias("uid"),
        pl.lit("street").alias("source_type"),
        pl.col("id").alias("source_id"),

        pl.col("name"),
        pl.col("name").alias("street"),
        pl.lit(None, dtype=pl.Utf8).alias("housenumber"),
        pl.lit(None, dtype=pl.Utf8).alias("postcode"),
        pl.lit(None, dtype=pl.Utf8).alias("city"),
        pl.col("city_id"),

        pl.col("lat"),
        pl.col("lon"),

        pl.lit(False).alias("is_city"),
        pl.col("is_street"),
        pl.lit(False).alias("is_place"),
    ])

    addresses_norm = addresses.select([
        pl.concat_str([pl.lit("address:"), pl.col("id")]).alias("uid"),
        pl.lit("address").alias("source_type"),
        pl.col("id").alias("source_id"),

        pl.col("name"),
        pl.col("street"),
        pl.col("housenumber"),
        pl.col("postcode"),
        pl.col("city"),
        pl.lit(None, dtype=pl.Int64).alias("city_id"),

        pl.col("lat"),
        pl.col("lon"),

        pl.lit(False).alias("is_city"),
        pl.lit(False).alias("is_street"),
        pl.col("is_place"),
    ])

    return pl.concat(
        [cities_norm, streets_norm, addresses_norm],
        how="vertical",
        rechunk=True,
    )


def drop_city_id(df: pl.DataFrame) -> pl.DataFrame:
    if "city_id" in df.columns:
        return df.drop("city_id")
    return df


def add_geo_point(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.struct(["lat", "lon"]).alias("location")
    )


