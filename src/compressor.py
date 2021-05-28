from typing import Dict, TypedDict
from utils.compressor.encode_data import encode_data
from utils.compressor.concat_symbols import concat_symbols
from utils.compressor.symbol_to_latin_encode import symbol_to_latin_encode
from tqdm import tqdm


class Compressor_Response(TypedDict):
    message: list
    indices: int


class Compressor():
    def __init__(self, data, dictionary, k):
        self.data = data.decode('latin_1')
        self.dictionary = dictionary
        self.k = pow(2, k)

    def run(self) -> Compressor_Response:
        message_size = len(self.data)-1
        if message_size < 1:
            return "There is no content to compress!"

        current_dictionary_value, idx, encoded_message = 256, 0, []

        while idx < message_size:
            symbol = encode_data(self.data, idx)
            next_symbol = encode_data(self.data, idx + 1)
            concatenated_symbols = concat_symbols(symbol, next_symbol)

            while concatenated_symbols in self.dictionary and idx < message_size:
                idx += 1

                symbol = concatenated_symbols

                if concatenated_symbols not in self.dictionary and current_dictionary_value < self.k and len(self.dictionary) < self.k:
                    self.dictionary[concatenated_symbols] = current_dictionary_value
                    current_dictionary_value += 1
                    encoded_message.append(
                        symbol_to_latin_encode(symbol, self.dictionary))
                concatenated_symbols = concat_symbols(
                    symbol, encode_data(self.data, idx + 1))

            if concatenated_symbols not in self.dictionary:
                if (current_dictionary_value < self.k) and len(self.dictionary) < self.k:
                    self.dictionary[concatenated_symbols] = current_dictionary_value
                    current_dictionary_value += 1
                encoded_message.append(
                    symbol_to_latin_encode(symbol, self.dictionary))
                if idx == message_size - 1:
                    encoded_message.append(
                        symbol_to_latin_encode(encode_data(self.data, idx + 1), self.dictionary))

            idx += 1

        response: Compressor_Response = {
            "message": encoded_message,
            "indices": len(encoded_message),
        }

        return response
