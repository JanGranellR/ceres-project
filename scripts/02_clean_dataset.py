import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'utils')

import os
import config
from utils import create_path, delete_path, copy_path

def rename_files() -> None:
    """
    Rename image files in the processed folder for each class.

    This function iterates through each class in the dataset, renames the image files,
    and prints information about the process.
    """
    for class_name in config.dataset["classes"]:
        print(f"[INFO] Renaming images for {class_name}")

        counter = 0
        for file in os.listdir(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name)):
            filename = f"{class_name}_{counter}.{config.dataset['classes_images_extension']}"
            original_filename = os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, file)

            os.rename(original_filename, os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, filename))
            counter += 1

        print(f"[INFO] Renaming images for {class_name} has successfully finished")

def remove_wrong_extensions() -> None:
    """
    Remove images with the wrong extension for each class.

    This function iterates through each class in the dataset, removes images with
    the wrong extension, and prints information about the process.
    """
    for class_name in config.dataset["classes"]:
        print(f"[INFO] Removing images with the wrong extension for {class_name}")

        # Iterate through and remove images with the wrong extension
        for file in os.listdir(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name)):
            if not file.endswith(config.dataset["classes_images_extension"]):
                os.remove(os.path.join(config.dataset["path"], config.dataset["path_raw"], class_name, file))

        print(f"[INFO] Removing images with the wrong extension for {class_name} has successfully finished")

def copy_data() -> None:
    """
    Copy data from the raw folder to the processed folder for each class.

    This function prepares folders, then iterates through each class in the dataset,
    creates paths, and copies data from the raw folder to the processed folder.
    """
    # Prepare folders
    delete_path(os.path.join(config.dataset["path"], config.dataset["path_processed"]), True)
    create_path(os.path.join(config.dataset["path"], config.dataset["path_processed"]))

    # Copy the data
    for class_name in config.dataset["classes"]:
        create_path(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name))
        copy_path(os.path.join(config.dataset["path"], config.dataset["path_raw"], class_name), os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name))

def clean() -> None:
    """
    Perform the cleaning process.

    This function calls the necessary functions to clean the dataset, including
    copying data, removing images with the wrong extension, and renaming files.
    """
    copy_data()
    remove_wrong_extensions()
    rename_files()

if __name__ == "__main__":
    clean()
