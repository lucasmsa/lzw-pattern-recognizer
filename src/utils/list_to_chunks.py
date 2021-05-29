def split_data_categories(one_dim_list: list):
    categories_chunk = {}

    for file_path in one_dim_list:
        category = file_path.split("/")[2]
        if category not in categories_chunk:
            categories_chunk[category] = [file_path]
        else:
            categories_chunk[category].append(file_path)

    return {
        "File paths": list(categories_chunk.values()),
        "Categories": list(categories_chunk.keys())
    }
