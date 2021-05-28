def encode_data(data, idx):
    if idx >= len(data):
        idx = len(data) - 1
    return str(data[idx]).encode('latin_1')
