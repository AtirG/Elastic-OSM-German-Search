import polars as pl

def clean_cities(df: pl.DataFrame) -> pl.DataFrame:
    """
    Cleans a cities DataFrame.

    Rules:
    - remove rows where name is null or empty
    - remove rows where lat is null
    - remove rows where lon is null
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

def add_is_city(cities: pl.DataFrame) -> pl.DataFrame:
    return cities.with_columns(
        pl.lit(1).alias("is_city")
    )
