import csv
import ast
import os

file_path = os.getenv("FILE_PATH", "./data/data.tsv")  # Default file path

def process_csv_to_object():
    facets_list = []

    # Auto-detect delimiter based on file extension
    delimiter = '\t' if file_path.endswith('.tsv') else ','

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)  # Read as a dictionary per row

        for row in reader:
            item_dict = {}  # Initialize as a dictionary
            for column_name, value in row.items():
                new_key = column_name.lower().replace(" ", "_")
                if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        pass

                # Convert specific values to an array (even if there's only one value)
                if (new_key == "motivation") and isinstance(value, str):
                    value = [item.strip() for item in value.split(",")]

                item_dict[new_key] = value

            facets_list.append(item_dict)

    return facets_list  # Return the list of parsed dictionaries