import random
import numpy as np


def split_train_test_filenames(file_paths: list, labels: list):
    x_test, y = [], []
    for images_list in file_paths:
        category = images_list[0].split("/")[-2]
        classification_image_photo_number = random.randint(1, 10)
        test_image = f"dataset/orl_faces/{category}/{classification_image_photo_number}.pgm"
        classification_image_idx = images_list.index(test_image)
        images_list.pop(classification_image_idx)
        x_test.append([test_image])
        y.append(category)

    return file_paths, x_test, y, y
