from .settings import SETTINGS
from .mappings import MAPPINGS

INDEX_NAME = "osm_addresses_de_v1"

INDEX_BODY = {
    "settings": SETTINGS,
    "mappings": MAPPINGS
}