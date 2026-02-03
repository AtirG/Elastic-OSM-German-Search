import polars as pl

def clean_streets(df: pl.DataFrame) -> pl.DataFrame:
    """
    Cleans a streets DataFrame.

    Rules:
    - remove rows without name (null or empty)
    - remove rows without lat
    - remove rows without lon
    """

    return (
        df
        .filter(
            pl.col("name").is_not_null() &
            pl.col("lat").is_not_null() &
            pl.col("lon").is_not_null()
        )
        .filter(
            pl.col("name").str.strip_chars() != ""
        )
    )


def add_is_street(streets: pl.DataFrame) -> pl.DataFrame:
    return streets.with_columns(
        pl.lit(True).alias("is_street")
    )