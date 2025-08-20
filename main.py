import json
import os
from src import es_client
from src import mappings
from src import process_csv_to_object

# Call the function to get the processed data
data = process_csv_to_object()

INDEX_NAME = os.getenv("INDEX_NAME", "ostrails")  # Default index

def init_index(index_name, mappings):
    """Creates an index if it doesn't exist yet"""
    try:
        if es_client.indices.exists(index=index_name):
            es_client.indices.delete(index=index_name)
    except Exception as e:
        print("[ERROR] initIndex", e)

    try:
        es_client.indices.create(index=index_name, body=mappings)
        print(f'Index "{index_name}" initialized')
    except Exception as e:
        print("[ERROR] initIndex", e)

def index_json():
    init_index(INDEX_NAME, mappings)
    print("data", json.dumps(data, indent=2))

    # Prepare bulk request
    bulk_ops = []
    for doc in data:
        bulk_ops.append({"index": {"_index": INDEX_NAME, "_id": doc["lodgde"]}})
        bulk_ops.append(doc)

    # Send data to Elasticsearch
    try:
        bulk_body = "\n".join([json.dumps(op) for op in bulk_ops]) + "\n"
        response = es_client.bulk(refresh=True, body=bulk_body)

        if response.get("errors"):
            print("[ERROR] Bulk indexing had issues:", json.dumps(response["items"], indent=2))
        else:
            print(f"Successfully indexed {len(response['items']) // 2} records")
    except Exception as e:
        print("[ERROR] Bulk indexing failed:", e)

if __name__ == "__main__":
    index_json()
