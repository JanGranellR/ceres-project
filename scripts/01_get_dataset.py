import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'utils')

import os
import config
import threading
from utils import stop_print, create_path, delete_path
from bbid import fetch_images_from_keyword

def main() -> None:
    """
    Main function to download images based on the configuration provided in the 'config' module.
    """

    # Prepare folders
    create_path(config.dataset["path"])
    create_path(config.dataset["path"] + "/" + config.dataset["path_raw"])

    for class_name in config.dataset["classes"]:
        create_path(os.path.join(config.dataset["path"], config.dataset["path_raw"], class_name))

    # Download images
    for class_name in config.dataset["classes"]:
        
        # Chech if the class already has all the images
        if len(os.listdir(os.path.join(config.dataset["path"], config.dataset["path_raw"], class_name))) >= config.dataset["classes_num_images"]:
            print(f"[INFO] Skipping {class_name} because it already has the images")
            continue

        print(f"[INFO] Downloading images for {class_name}")

        for keyword in config.dataset["classes_keywords"][class_name]:
            # Call the function
            fetch_images_from_keyword(threading.BoundedSemaphore(5), threading.Semaphore(), keyword, config.dataset["path"] + "/" + config.dataset["path_raw"] + "/" + class_name, "", config.dataset["classes_num_images"])

        print(f"[INFO] Downloading images for {class_name} has successfully finished")
        
if __name__ == "__main__":
    main()