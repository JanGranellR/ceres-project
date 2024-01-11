import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'utils')

import os
import config
import random
import shutil
import fastdup
from utils import create_path, delete_path, copy_path, delete_files

def separate_files() -> None:
    """
    Separates files into training and test sets for each class in the dataset.
    """

    for class_name in config.dataset["classes"]:
        # Prepare folders
        delete_path(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_training"]), True)
        delete_path(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_test"]), True)
        
        create_path(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_training"]))
        create_path(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_test"]))

        all_files = os.listdir(os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name))
        
        random.shuffle(all_files)

        # Divide the files into two lists based on the split index
        split_index = int(len(all_files) * config.dataset["classes_images_split_ratio"])
        
        files_folder1 = all_files[:split_index]
        files_folder2 = all_files[split_index:]

        # Move files to the respective output folders
        input_folder = os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name)
        output_folder_training = os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_training"])
        output_folder_test = os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name, config.dataset["path_test"])

        for file in files_folder1:
            if os.path.isfile(os.path.join(input_folder, file)):
                source_path = os.path.join(input_folder, file)
                destination_path = os.path.join(output_folder_training, file)
                
                shutil.move(source_path, destination_path)

        for file in files_folder2:
            if os.path.isfile(os.path.join(input_folder, file)):
                source_path = os.path.join(input_folder, file)
                destination_path = os.path.join(output_folder_test, file)

                shutil.move(source_path, destination_path)

def _fastdup() -> None:
    """
    Encapsulates the main logic for processing datasets using Fastdup.

    This function initiates the Fastdup workflow, including initializing the Fastdup object, running the analysis, handling output galleries, and removing invalid and outlier instances.
    """

    # Prepare folders
    delete_path(os.path.join(config.dataset["path"], config.dataset["path_fastdup"]), True)

    for class_name in config.dataset["classes"]:
        print(f"[INFO] Fastdup running for {class_name}")

        # Get the paths to the processed class data and the Fastdup working directory
        dir = os.path.join(config.dataset["path"], config.dataset["path_processed"], class_name)
        work_dir = os.path.join(config.dataset["path"], config.dataset["path_fastdup"], class_name)

        create_path(work_dir)

        # Instantiate a Fastdup object
        fd = fastdup.create(work_dir=work_dir, input_dir=dir)

        # Run Fastdup on the image data
        fd.run(data_type="image", overwrite=True, verbose=False)

        # If the 'export' flag is set
        if config.dataset["fastdup"]["export"] == True:
            fd.vis.duplicates_gallery()
            fd.vis.outliers_gallery()

        # Remove invalid instances and outliers detected by Fastdup
        delete_files(fd.invalid_instances()["filename"].to_list())
        delete_files(fd.outliers()["filename_outlier"].to_list())

        print(f"[INFO] Fastdup running for {class_name} has successfully finished")

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
    _fastdup()
    separate_files()

if __name__ == "__main__":
    clean()
