import polars as pl
import string
def clean_addresses_geo(addresses: pl.DataFrame) -> pl.DataFrame:
    """
    Remove rows without latitude or longitude.
    """
    return addresses.filter(
        pl.col("lat").is_not_null() &
        pl.col("lon").is_not_null()
    )


def clean_addresses_geo_and_content(addresses: pl.DataFrame) -> pl.DataFrame:
    return addresses.filter(
        # must have geo
        pl.col("lat").is_not_null() &
        pl.col("lon").is_not_null() &

        # must have at least one meaningful field
        pl.any_horizontal([
            pl.col("name").is_not_null() & (pl.col("name").str.len_chars() > 0),
            pl.col("housenumber").is_not_null() & (pl.col("housenumber").str.len_chars() > 0),
            pl.col("street").is_not_null() & (pl.col("street").str.len_chars() > 0),
            pl.col("postcode").is_not_null() & (pl.col("postcode").str.len_chars() > 0),
            pl.col("city").is_not_null() & (pl.col("city").str.len_chars() > 0),
        ])
    )


def add_is_place(addresses: pl.DataFrame) -> pl.DataFrame:
    return addresses.with_columns(
        (
            pl.col("name").is_not_null() &
            (pl.col("name").str.len_chars() > 0)
        ).cast(pl.Int8).alias("is_place")
    )

def explode_housenumber_lists(addresses: pl.DataFrame) -> pl.DataFrame:
    return (
        addresses
        .with_columns(
            pl.when(
                pl.col("housenumber").is_not_null() &
                pl.col("housenumber").str.contains(r"[;,/]")
            )
            .then(
                pl.col("housenumber")
                .str.to_lowercase()
                .str.replace_all(r"\s+", "")
                .str.replace_all(r"[;/]", ",")
                .str.split(",")
            )
            .otherwise(
                pl.when(pl.col("housenumber").is_not_null())
                .then(pl.concat_list([pl.col("housenumber")]))
                .otherwise(None)
            )
            .alias("housenumber_split")
        )
        .explode("housenumber_split")
        .with_columns(
            pl.col("housenumber_split").alias("housenumber")
        )
        .drop("housenumber_split")
    )


def expand_housenumber_range(value: str) -> list[str]:
    if not isinstance(value, str) or not value:
        return []

    value = value.lower().replace(" ", "")

    if "-" not in value:
        return [value]

    start, end = value.split("-", 1)

    if start[:-1].isdigit() and end[:-1].isdigit() and start[:-1] == end[:-1]:
        s_letter, e_letter = start[-1], end[-1]
        if s_letter in string.ascii_lowercase and e_letter in string.ascii_lowercase:
            base = start[:-1]
            return [
                f"{base}{c}"
                for c in string.ascii_lowercase[
                    string.ascii_lowercase.index(s_letter):
                    string.ascii_lowercase.index(e_letter) + 1
                ]
            ]

    if start.isdigit() and end.isdigit():
        s, e = int(start), int(end)
        if e - s <= 20:
            return [str(i) for i in range(s, e + 1)]

    return [value]


#we run only this. it has the other nested inside
def expand_housenumber_ranges_df(
    df: pl.DataFrame,
    column: str = "housenumber",
) -> pl.DataFrame:
    return (
        df
        .with_columns(
            pl.col(column)
              .map_elements(expand_housenumber_range)
              .alias("_hn_split")
        )
        .explode("_hn_split")
        .with_columns(
            pl.col("_hn_split").alias(column)
        )
        .drop("_hn_split")
    )





def nullify_too_long_housenumbers(addresses: pl.DataFrame) -> pl.DataFrame:
    return addresses.with_columns(
        pl.when(
            pl.col("housenumber").is_not_null() &
            (pl.col("housenumber").str.len_chars() > 20)
        )
        .then(pl.lit(None, dtype=pl.Utf8))
        .otherwise(pl.col("housenumber"))
        .alias("housenumber")
    )


def nullify_long_postcodes(addresses: pl.DataFrame) -> pl.DataFrame:
    return addresses.with_columns(
        pl.when(
            pl.col("postcode").is_not_null() &
            (pl.col("postcode").str.len_chars() >= 6)
        )
        .then(None)
        .otherwise(pl.col("postcode"))
        .alias("postcode")
    )

def nullify_short_postcodes(addresses: pl.DataFrame) -> pl.DataFrame:
    return addresses.with_columns(
        pl.when(
            pl.col("postcode").is_not_null() &
            (pl.col("postcode").str.len_chars() <= 4)
        )
        .then(None)
        .otherwise(pl.col("postcode"))
        .alias("postcode")
    )