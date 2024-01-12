import os
from config import config
import joblib
import cv2 as cv
import numpy as np

class ImagePredictor(object):
    def __init__(self, model_path: str = None) -> None:
        """Initialize the ImagePredictor object with a pre-trained model.

        Parameters:
        - model_path (str): Path to the pre-trained model.
        """

        self.model = joblib.load(model_path)

    def import_image(self, image_path: str = None) -> np.ndarray:
        """
        Import and preprocess an image.

        Parameters:
        - image_path (str): Path to the image file.

        Returns:
        - np.ndarray: Flattened and resized image.
        """

        img = cv.imread(image_path)
        img = cv.resize(img, (100, 100))
        img = img.flatten()

        return img

    def predict(self, image_path: str = None, confidence_threshold: float = 0.8) -> None:
        """
        Predict the label of an image.

        Parameters:
        - image_path (str): Path to the image file.
        - confidence_threshold (float): Minimum confidence level for predictions.
        """

        results = self.model.predict_proba([self.import_image(image_path)])[0]

        print("\nResults:")
        print("----------------------------------------------------")
        print(f"Predicted Class: '{self.model.classes_[np.argmax(results)]}'")
        print("Confidence Score:")

        for i in range(len(results.tolist())):
            print(f"    - '{self.model.classes_[i]}': {results.tolist()[i]}")

if __name__ == '__main__':
    image_path = input("Enter the path to the image: ")

    # Check if path is none
    if image_path is None:
        print("[INFO] Path not specified")
        exit()

    # Check if path exists
    if not os.path.exists(image_path):
        print("[INFO] Path does not exist")
        exit()

    predictor = ImagePredictor(
                    model_path = os.path.join(config.model["path"], config.model["path_models"], config.model["name"])
                )
    predictor.predict(image_path)
