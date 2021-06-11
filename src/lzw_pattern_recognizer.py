import os
import numpy as np
from math import e
from tqdm import tqdm
from typing import Dict
from sklearn import svm
from sklearn import datasets
from compressor import Compressor
from utils.list_to_chunks import split_data_categories
from utils.split_train_test_filenames import split_train_test_filenames

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
        data_categories = split_data_categories(self.data["filenames"])
        x, y = data_categories["File paths"], list(
            data_categories["Categories"])

        self.x_train, self.x_test, self.y_train, self.y_test = split_train_test_filenames(
            x, y
        )

        # clf = svm.SVC(kernel='linear', C=1).fit(self.x_train, self.x_test)
        # print(clf.score(self.x_test, self.y_test))

    def generate_classification_results(self) -> Dict:
        self.compressed_classification_categories = {}

        for test_slice in tqdm(self.x_test):
            [test_file] = test_slice
            test_category = test_file.split("/")[2]
            original_file = open(test_file, "rb").read()
            for category, category_dictionary in self.categories_dictionary.items():
                compressor = Compressor(
                    data=original_file, dictionary=category_dictionary, k=10, is_classfication=True)
                compressor_response = compressor.run()
                if test_category not in self.compressed_classification_categories:
                    self.compressed_classification_categories[test_category] = {
                    }
                self.compressed_classification_categories[test_category][
                    category] = compressor_response["indices"]

    def generate_dictionary_for_database_categories(self) -> Dict:
        self.categories_dictionary = {}
        self.compression_indices_dictionary = {}

        for train_slice in tqdm(self.x_train):
            for file_path in train_slice:
                category = file_path.split("/")[2]
                if category not in self.categories_dictionary:
                    self.categories_dictionary[category] = self.init_code_dictionary(
                    )
                original_file = open(file_path, "rb").read()
                compressor = Compressor(
                    data=original_file, dictionary=self.categories_dictionary[category], k=10)
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
lzw_pattern_recognizer.generate_classification_results()
