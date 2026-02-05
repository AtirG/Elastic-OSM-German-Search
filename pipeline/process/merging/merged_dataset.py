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

        pl.col("lat"),
        pl.col("lon"),

        pl.lit(1, dtype=pl.Int8).alias("is_city"),
        pl.lit(0, dtype=pl.Int8).alias("is_street"),
        pl.lit(0, dtype=pl.Int8).alias("is_place"),
    ])

    streets_norm = streets.select([
        pl.concat_str([pl.lit("street:"), pl.col("id")]).alias("uid"),
        pl.lit("street").alias("source_type"),
        pl.col("id").alias("source_id"),

        pl.lit(None, dtype=pl.Utf8).alias("name"),
        pl.col("name").alias("street"),
        pl.lit(None, dtype=pl.Utf8).alias("housenumber"),
        pl.lit(None, dtype=pl.Utf8).alias("postcode"),
        pl.lit(None, dtype=pl.Utf8).alias("city"),

        pl.col("lat"),
        pl.col("lon"),

        pl.lit(0, dtype=pl.Int8).alias("is_city"),
        pl.lit(1, dtype=pl.Int8).alias("is_street"),
        pl.lit(0, dtype=pl.Int8).alias("is_place"),
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

        pl.col("lat"),
        pl.col("lon"),

        pl.lit(0, dtype=pl.Int8).alias("is_city"),
        pl.lit(0, dtype=pl.Int8).alias("is_street"),
        pl.lit(1, dtype=pl.Int8).alias("is_place"),
    ])

    return pl.concat(
        [cities_norm, streets_norm, addresses_norm],
        how="vertical",
        rechunk=True,
    )



