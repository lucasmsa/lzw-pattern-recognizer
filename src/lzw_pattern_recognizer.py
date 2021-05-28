import os
import numpy as np
from tqdm import tqdm
from sklearn import svm
from typing import Dict
from sklearn import datasets
from compressor import Compressor
from utils.list_to_chunks import list_to_chunks
from sklearn.model_selection import train_test_split

INITIAL_DICTIONARY_SIZE = 256


class Lzw_Pattern_Recognizer():
    def __init__(self, database_path, output_path):
        self.database_path = database_path
        self.output_path = output_path

    def init_code_dictionary(self):
        dictionary = {}
        for i in range(INITIAL_DICTIONARY_SIZE):
            dictionary[i.to_bytes(1, 'big')] = i

        return dictionary

    def split_dataset(self):
        self.data = datasets.load_files(self.database_path)
        x, y = np.array(list_to_chunks(self.data["filenames"], 10)), np.array(
            self.data["target_names"])

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            x, y, test_size=0.5, random_state=0)

    def generate_dictionary_for_database_categories(self) -> Dict:
        self.categories_dictionary = {}
        self.compression_indices_dictionary = {}

        for train_slice in tqdm(self.x_train):
            for file_path in train_slice:
                category = file_path.split("/")[2]
                if category not in self.categories_dictionary:
                    self.categories_dictionary[category] = \
                        self.init_code_dictionary()

                original_file = open(file_path, "rb").read()
                compressor = Compressor(
                    data=original_file, dictionary=self.categories_dictionary[category], k=16)
                compressor_response = compressor.run()
                self.compression_indices_dictionary[file_path] = compressor_response["indices"]

        return {
            "Categories dictionary": self.categories_dictionary,
            "Compression Indices per image": self.compression_indices_dictionary
        }


lzw_pattern_recognizer = Lzw_Pattern_Recognizer(
    database_path="dataset/orl_faces",
    output_path="output"
)

lzw_pattern_recognizer.split_dataset()
lzw_pattern_recognizer.generate_dictionary_for_database_categories()
