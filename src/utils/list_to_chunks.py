def list_to_chunks(one_dim_list: list, size: int):
    new_list = []
    for i in range(0, len(one_dim_list), size):
        new_list.append(one_dim_list[i:i + size])
    return new_list
