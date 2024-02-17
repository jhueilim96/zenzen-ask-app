import os
import typesense

config = {
    "nodes": [{"host": "localhost", "port": "8108", "protocol": "http"}],
    "api_key": os.environ.get("typesense_key"),
    "connection_timeout_seconds": 2,
}

client = typesense.Client(config)

if __name__ == "__main__":
    pass
