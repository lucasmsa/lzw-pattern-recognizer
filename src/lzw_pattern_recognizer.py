import os
import numpy as np
from sklearn import svm
from sklearn import datasets
from utils.list_to_chunks import list_to_chunks
from sklearn.model_selection import train_test_split


class Lzw_Pattern_Recognizer():
    def __init__(self, database_path, output_path):
        self.database_path = database_path
        self.output_path = output_path

    def split_dataset(self):
        data = datasets.load_files(self.database_path)
        x, y = np.array(list_to_chunks(data["filenames"], 10)), np.array(
            data["target_names"])

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.5, random_state=0)


lzw_pattern_recognizer = Lzw_Pattern_Recognizer(
    database_path="dataset/orl_faces",
    output_path="output"
)

lzw_pattern_recognizer.split_dataset()
