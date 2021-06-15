import os
import numpy as np
from math import e
from tqdm import trange
from typing import Dict
from sklearn import svm
from colorama import Fore
from statistics import mean
from sklearn import datasets
from compressor import Compressor
from utils.list_to_chunks import split_data_categories
from utils.split_train_test_filenames import split_train_test_filenames as cross_validation

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
        x, y = data_categories["File paths"], list(data_categories["Categories"])

        self.x_train, self.x_test, self.y_train, self.y_test = cross_validation(
            x, y
        )

    def generate_classification_results(self):
        self.compressed_classification_categories = {}

        progress_bar = trange(len(self.x_train), position=0, leave=True)

        for row, test_slice in enumerate(self.x_test):
            [test_file] = test_slice
            test_category = test_file.split("/")[2]
            original_file = open(test_file, "rb").read()
            best_compression = {
                "category": "",
                "indices": float("inf")
            }
            for category, category_dictionary in self.categories_dictionary.items():
                compressor = Compressor(
                    data=original_file, dictionary=category_dictionary, k=10, is_classfication=True)
                compressor_response = compressor.run()
                if compressor_response["indices"] < best_compression["indices"]:
                    best_compression["indices"] = compressor_response["indices"]
                    best_compression["category"] = category

            self.compressed_classification_categories[test_category] = best_compression
            self.x_test[row][0] = best_compression["indices"]
            progress_bar.update(1)

        progress_bar.close()

        print(
            f"X_TRAIN: {self.x_train}, X_TEST: {self.x_test}, Y_TRAIN: {self.y_train}, Y_TEST: {self.y_test}")
        print(
            f"X_TRAIN: {len(self.x_train)}, X_TEST: {len(self.x_test)}, Y_TRAIN: {len(self.y_train)}, Y_TEST: {len(self.y_test)}")

    def generate_dictionary_for_database_categories(self):
        self.categories_dictionary = {}
        self.x_train_means = []

        progress_bar = trange(len(self.x_train), position=0, leave=True)

        for row, train_slice in enumerate(self.x_train):
            for column, file_path in enumerate(train_slice):
                category = file_path.split("/")[2]
                if category not in self.categories_dictionary:
                    self.categories_dictionary[category] = self.init_code_dictionary(
                    )
                original_file = open(file_path, "rb").read()[14:]
                compressor = Compressor(
                    data=original_file, dictionary=self.categories_dictionary[category], k=10)
                compressor_response = compressor.run()
                self.x_train[row][column] = compressor_response["indices"]
            self.x_train_means.append([mean(self.x_train[row])])
            progress_bar.update(1)

        progress_bar.close()


lzw_pattern_recognizer = Lzw_Pattern_Recognizer(
    database_path="dataset/orl_faces",
    output_path="output"
)

lzw_pattern_recognizer.split_dataset()
lzw_pattern_recognizer.generate_dictionary_for_database_categories()
lzw_pattern_recognizer.generate_classification_results()