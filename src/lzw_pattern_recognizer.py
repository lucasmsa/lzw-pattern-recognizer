import time
from tqdm import tqdm
from sklearn import datasets
from compressor import Compressor
from utils.generate_graphs import generate_graphs
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

    def generate_classification_results(self, k: int):
        self.compressed_classification_categories = {}
        hit_rate = 0

        for test_slice in tqdm(self.x_test):
            [test_file] = test_slice
            test_category = test_file.split("/")[2]
            original_file = open(test_file, "rb").read()
            best_compression = {
                "category": "",
                "indices": float("inf")
            }
            for category, category_dictionary in self.categories_dictionary.items():
                compressor = Compressor(
                    data=original_file, dictionary=category_dictionary, k=k, is_classfication=True)
                compressor_response = compressor.run()
                if compressor_response["indices"] < best_compression["indices"]:
                    best_compression["indices"] = compressor_response["indices"]
                    best_compression["category"] = category

            self.compressed_classification_categories[test_category] = best_compression["category"]
            if test_category == best_compression["category"]:
                hit_rate += 1

        return hit_rate/len(self.x_test)

    def generate_dictionary_for_database_categories(self, k: int):
        self.categories_dictionary = {} 

        for train_slice in tqdm(self.x_train):
            for file_path in train_slice:
                category = file_path.split("/")[2]
                if category not in self.categories_dictionary:
                    self.categories_dictionary[category] = self.init_code_dictionary(
                    )
                original_file = open(file_path, "rb").read()[14:]
                compressor = Compressor(
                    data=original_file, dictionary=self.categories_dictionary[category], k=k)
                compressor.run()

lzw_pattern_recognizer = Lzw_Pattern_Recognizer(
    database_path="dataset/orl_faces",
    output_path="output"
)

lzw_pattern_recognizer.split_dataset()
hit_rates_per_k, time_spent_per_k = [], []
for k in range(9, 17):
    k_start_time = time.time()  
    lzw_pattern_recognizer.generate_dictionary_for_database_categories(k)
    hit_rates_per_k.append(lzw_pattern_recognizer.generate_classification_results(k))
    k_end_time = time.time()
    time_spent_per_k.append(round(k_end_time - k_start_time, 2))
    print(f"\nCompression for a {k} bits dictionary completed ✅\n")
    
generate_graphs(hit_rates_per_k, time_spent_per_k, (9, 17))