import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'utils')

import os
import config
import fastdup
from utils import create_path, delete_path, delete_files

def main() -> None:
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

if __name__ == '__main__':
    main()