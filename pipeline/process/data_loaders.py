import polars as pl

def load_addresses():
    return pl.read_csv(
        "data/raw/addresses.csv",
        schema={
            "id": pl.Int64,
            "name": pl.String,
            "building": pl.String,
            "housenumber": pl.String,
            "street": pl.String,
            "postcode": pl.String,
            "city": pl.String,
            "lat": pl.Float64,
            "lon": pl.Float64,
        }
    )

def load_cities():
    return (
        pl.read_csv(
            "data/raw/cities.csv",
            schema={
                "id": pl.Int64,
                "name": pl.String,
                "place": pl.String,
                "lat": pl.Float64,
                "lon": pl.Float64,
                "other_tags": pl.String,
            }
        )
        .drop("other_tags")
    )

def load_streets():
    return (
        pl.read_csv(
            "data/raw/streets.csv",
            schema={
                "id": pl.Int64,
                "name": pl.String,
                "highway": pl.String,
                "lat": pl.Float64,
                "lon": pl.Float64,
                "city_id": pl.Int64,
                "other_tags": pl.String,
            }
        )
        .drop("other_tags")
    )


def load_postcode_enriched():
    return pl.read_csv(
        "pipeline/process/merged_with_postcode_enriched.csv",
        schema={
            "uid": pl.String,
            "lat": pl.Float64,
            "lon": pl.Float64,
            "postcode": pl.String,
            "postcode_enriched": pl.String,
        }
    ).select(["uid", "postcode_enriched"])

def load_admin_enriched():
    return pl.read_csv(
        "data/processed/admin_enriched.csv",
        schema={
            "uid": pl.String,
            "admin4_name": pl.String,
            "admin6_name": pl.String,
            "admin8_name": pl.String,
        }
    )

def load_geo_enriched():
    return pl.read_csv(
        "data/processed/geo_enriched.csv",
        schema={
            "uid": pl.String,
            "postcode": pl.String,
            "postcode_enriched": pl.String,
            "admin4_name": pl.String,
            "admin6_name": pl.String,
            "admin8_name": pl.String,
        }
    )

def load_merged_dataset():
    return pl.read_csv(
        "data/processed/merged_dataset.csv",
        schema={
            "uid": pl.String,
            "source_type": pl.String,
            "source_id": pl.Int64,

            "name": pl.String,
            "street": pl.String,
            "housenumber": pl.String,
            "postcode": pl.String,
            "city": pl.String,

            "lat": pl.Float64,
            "lon": pl.Float64,

            "is_city": pl.Boolean,
            "is_street": pl.Boolean,
            "is_place": pl.Boolean,
        }
    )


def load_final_addresses() -> pl.DataFrame:
    return pl.read_csv(
        "data/processed/final_addresses.csv",
        schema={
            "uid": pl.String,
            "source_type": pl.String,
            "source_id": pl.Int64,

            "name": pl.String,
            "street": pl.String,
            "housenumber": pl.String,
            "postcode": pl.String,
            "city": pl.String,

            "lat": pl.Float64,
            "lon": pl.Float64,

            "is_city": pl.Boolean,
            "is_street": pl.Boolean,
            "is_place": pl.Boolean,

            "country_code": pl.String,
            "country_name": pl.String,
            "display_address": pl.String,

            "is_full_address": pl.Boolean,
            "merged_address": pl.String,
        },
    )





def pl_wide_view(
    table_width: int = 1000,
    col_width: int = 200,
    rows: int = 20,
    cols: int = 50,
):
    pl.Config.set_tbl_width_chars(table_width)
    pl.Config.set_fmt_str_lengths(col_width)
    pl.Config.set_tbl_rows(rows)
    pl.Config.set_tbl_cols(cols)

def widen_string_display(max_len: int = 200) -> None:
    pl.Config.set_fmt_str_lengths(max_len)