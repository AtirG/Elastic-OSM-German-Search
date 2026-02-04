import polars as pl

def add_country_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns([
        pl.lit("DE").alias("country_code"),
        pl.lit("Germany").alias("country_name"),
    ])


def add_display_address(df: pl.DataFrame) -> pl.DataFrame:
    street_full = pl.when(
        pl.col("street").is_not_null() & (pl.col("street") != "")
    ).then(
        pl.concat_str(
            [
                pl.col("street"),
                pl.when(pl.col("housenumber").is_not_null() & (pl.col("housenumber") != ""))
                  .then(pl.concat_str([pl.lit(" "), pl.col("housenumber")]))
                  .otherwise(pl.lit(""))
            ]
        )
    ).otherwise(None)

    return df.with_columns(
        pl.concat_str(
            [
                pl.col("name"),
                street_full,
                pl.col("postcode"),
                pl.col("city"),
                pl.col("country_name"),
            ],
            separator=", ",
            ignore_nulls=True,
        ).alias("display_address")
    )




def add_merged_address(df: pl.DataFrame) -> pl.DataFrame:
    street_full = pl.when(
        pl.col("street").is_not_null() & (pl.col("street") != "")
    ).then(
        pl.concat_str(
            [
                pl.col("street"),
                pl.when(
                    pl.col("housenumber").is_not_null() & (pl.col("housenumber") != "")
                )
                .then(pl.concat_str([pl.lit(" "), pl.col("housenumber")]))
                .otherwise(pl.lit(""))
            ]
        )
    ).otherwise(None)

    return df.with_columns(
        pl.concat_str(
            [
                pl.col("name"),
                street_full,
                pl.col("postcode"),
                pl.col("city"),
                pl.col("country_name"),
            ],
            separator=" ",
            ignore_nulls=True,
        ).alias("merged_address")
    )





def add_is_full_address(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        (
            (pl.col("street").is_not_null() & (pl.col("street") != "")) &
            (pl.col("housenumber").is_not_null() & (pl.col("housenumber") != "")) &
            (pl.col("postcode").is_not_null() & (pl.col("postcode") != "")) &
            (pl.col("city").is_not_null() & (pl.col("city") != ""))
        ).alias("is_full_address")
    )




def export_final_addresses(df: pl.DataFrame) -> None:
    (
        df
        .drop("location")
        .write_csv("data/processed/final_addresses.csv")
    )

def export_final_addresses_no_location(df: pl.DataFrame) -> None:
    (
        df.write_csv("data/processed/final_addresses.csv")
    )