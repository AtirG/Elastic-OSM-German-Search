from es.client import es
from es.indexes.osm_addresses_de import INDEX_NAME,INDEX_BODY
import time

GLOBAL_ALIAS = "osm_addresses_global"

def wait_for_es(timeout=60):
    start = time.time()
    while True:
        try:
            if es.ping():
                print("Elasticsearch is ready")
                return
        except ConnectionError:
            pass

        if time.time() - start > timeout:
            raise RuntimeError("Elasticsearch not ready in time")

        time.sleep(2)


def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=INDEX_BODY)
        print(f"Created index: {INDEX_NAME}")
    else:
        print(f"Index already exists: {INDEX_NAME}")


def create_global_alias():
    if not es.indices.exists_alias(name=GLOBAL_ALIAS):
        es.indices.update_aliases(
            body={
                "actions": [
                    {"add": {"index": INDEX_NAME, "alias": GLOBAL_ALIAS}}
                ]
            }
        )
        print(f"Alias '{GLOBAL_ALIAS}' → {INDEX_NAME}")
    else:
        print(f"Alias already exists: {GLOBAL_ALIAS}")


if __name__ == "__main__":
    wait_for_es()
    create_index()
    create_global_alias()