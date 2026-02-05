import polars as pl

def drop_rows_without_postcode(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        pl.col("postcode").is_not_null()
        & (pl.col("postcode") != "")
    )


def add_country_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns([
        pl.lit("DE").alias("country_code"),
        pl.lit("Germany").alias("country_name"),
    ])


def fill_city_from_admin(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.when(pl.col("city").is_null() & pl.col("admin8_name").is_not_null())
          .then(pl.col("admin8_name"))
          .when(pl.col("city").is_null() & pl.col("admin6_name").is_not_null())
          .then(pl.col("admin6_name"))
          .when(pl.col("city").is_null() & pl.col("admin4_name").is_not_null())
          .then(pl.col("admin4_name"))
          .otherwise(pl.col("city"))
          .alias("city")
    )


def drop_address_rows_without_city(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        ~(
            (pl.col("source_type") == "address") &
            (pl.col("city").is_null() | (pl.col("city") == ""))
        )
    )



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
        )
        .cast(pl.Int8)
        .alias("is_full_address")
    )





def export_final_addresses(df: pl.DataFrame) -> None:
    (
        df.write_csv("data/processed/final_addresses.csv")
    )