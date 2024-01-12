import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'utils')

import os
import time
import config
import joblib
import cv2 as cv
import numpy as np
import concurrent.futures
from sklearn.svm import SVC
from utils import create_path, delete_path

def import_images_thread(path: str, label: str, files: list[str]) -> list:
    """
        Import images from a specified path and assign labels (using a Thread).

        Parameters:
        - path (str): The path to the images.
        - label (str): The label assigned to the images.
        - files (list[str]): The list of files.

        Returns:
        - list: List containing images and labels.
    """

    images = [].copy()
    labels = [].copy()

    for file in files:
        # Make sure we just use images
        if os.path.isfile(os.path.join(path, file)):
            img = cv.imread(os.path.join(path, file))
            img = cv.resize(img, (100, 100))

            images.append(img.flatten())
            labels.append(label)

    return images, labels

class Algorithm(object):
    
    def __init__(self, *, base_path: str, model_path: str = "models",  model_name: str = "svc_model.joblib", classes: list[str], classes_path: str, classes_path_training: str, classes_path_test: str) -> None:
        """
        Initialize the Algorithm class.

        Parameters:
        - base_path (str): The base path for the model and dataset.
        - model_path (str): The path where the model will be saved.
        - model_name (str): The name of the model file.
        - classes (list): List of class names.
        - classes_path (str): The path to the processed dataset.
        - classes_path_training (str): The subpath for the training data.
        - classes_path_test (str): The subpath for the test data.
        """

        self.base_path = base_path
        self.classes = classes
        self.model_name = model_name
        self.model_path = model_path
        self.classes_path = classes_path
        self.classes_path_training = classes_path_training
        self.classes_path_test = classes_path_test

        self.model = SVC(C = 2, probability = True)

        # Initialize lists to store training and test data
        self.training_labels = [].copy()
        self.training_images = [].copy()
        self.test_labels = [].copy()
        self.test_images = [].copy()
    
    def import_images(self, *, path: str = None, label: str = "other") -> list:
        """
        Import images from a specified path and assign labels.

        Parameters:
        - path (str): The path to the images.
        - label (str): The label assigned to the images.

        Returns:
        - list: List containing images and labels.
        """

        images = [].copy()
        labels = [].copy()
        threads = [].copy()

        # Check if path is none
        if path is None:
            print("[INFO] Path not specified")
            return []

        # Check if path exists
        if not os.path.exists(path):
            print("[INFO] Path does not exist")
            return []

        print(f"[INFO] Importing images for label {label}")

        files = os.listdir(path)
        time_start = time.time()

        # Import images from filesystem using multiple threads
        with concurrent.futures.ProcessPoolExecutor() as executor:

            # Creates threads to import images (5 images per thread)
            while len(files) > 0:
                threads.append(executor.submit(import_images_thread, path, label, files[: 5]))

                files = files[5: ]
            
            concurrent.futures.wait(threads)

            # Combine the images and their labels
            for t in threads:
                images_tmp, labels_tmp = t.result()

                images.extend(images_tmp)
                labels.extend(labels_tmp)        
        
        print(f"[INFO] Importing images for label {label} has successfully finished in {time.time() - time_start} seconds")
        
        return images, labels

    def model_test(self) -> None:
        """
        Test the trained model on the test dataset.
        """

        print("[INFO] Starting model tests")

        for class_name in self.classes:
            images, labels = self.import_images(path = os.path.join(self.classes_path, class_name, self.classes_path_test), label = class_name)
            
            correct_predictions = 0

            predictions_results = {}

            for i in self.classes:
                predictions_results[i] = 0

            for x, image in enumerate(images):
                result = self.model.predict([image])

                predictions_results[result[0]] = predictions_results[result[0]] + 1
                                
                if result[0] == labels[x]:
                    correct_predictions += 1

            print(f"[TEST] Correct predictions for class {class_name}: {round((correct_predictions/ len(images)) * 100)} %")
            print(f"[TEST] Predictions results: {predictions_results}")

    def model_save(self) -> None:
        """
        Save the trained model to a specified file path.
        """

        print(f"[INFO] Saving the model to {self.model_name}")
        
        delete_path(self.base_path + "/" + self.model_path, True)
        create_path(self.base_path + "/" + self.model_path)
        
        joblib.dump(self.model, os.path.join(self.base_path, self.model_path, self.model_name))
        
        print("[INFO] Model saved successfully")

    def model_run(self) -> None:
        """
        Train the model using the provided dataset.
        """

        for class_name in self.classes:
            images, labels = self.import_images(path = os.path.join(self.classes_path, class_name, self.classes_path_training), label = class_name)

            self.training_images.extend(images)
            self.training_labels.extend(labels)

        print("[INFO] Running training algorithm")

        time_start = time.time()

        # Convert the list of 1D arrays to a 2D array
        self.training_images = np.vstack(self.training_images)

        self.model.fit(self.training_images, self.training_labels)

        print(f"[INFO] Running training algorithm has successfully finished in {time.time() - time_start} seconds")

if __name__ == '__main__':
    a = Algorithm(
        base_path = config.model["path"],
        model_path = config.model["path_models"],
        model_name = config.model["name"],
        classes = config.dataset["classes"],
        classes_path = os.path.join(config.dataset["path"], config.dataset["path_processed"]),
        classes_path_training = config.dataset["path_training"],
        classes_path_test = config.dataset["path_test"]
    )
    a.model_run()
    a.model_save()
    a.model_test()