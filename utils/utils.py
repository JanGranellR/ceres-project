import os
import sys
import shutil

def stop_print(func, *args, **kwargs):
    """
    Temporarily suppress the standard output while executing a function.

    Parameters:
    - func (callable): The function to be executed without printing to stdout.
    - *args: Variable positional arguments to be passed to the function.
    - **kwargs: Variable keyword arguments to be passed to the function.
    """
    
    # Redirect stdout to os.devnull to suppress printing
    with open(os.devnull, "w") as devNull:
        original_stdout = sys.stdout
        sys.stdout = devNull

        try:
            # Execute the provided function without printing to stdout
            func(*args, **kwargs)

        finally:
            # Restore the original stdout after the function execution
            sys.stdout = original_stdout

def create_path(p: str = None) -> bool:
    """
    Create a directory path if it does not exist.

    Parameters:
    - p (str): The path to be created.

    Returns:
    - bool: True if the path is created or already exists, False otherwise.
    """

    # Check if the path is not specified
    if p == None:
        print("[INFO] No path specified")
        return False
    
    # Check if the path already exists
    if os.path.exists(p):
        print(f"[INFO] Path {p} already exists")
        return True
    
    try:
        # Create the directory path
        os.makedirs(p)
        print(f"[INFO] Path {p} created successfully")
        return True

    except Exception as e:
        # Handle potential errors during path creation
        print(f"[ERROR] Unable to create path {p}: {e}")
        return False

def delete_path(p: str = None, f: bool = False) -> bool:
    """
    Delete a directory path if it does exist.

    Parameters:
    - p (str): The path to be deleted.

    Returns:
    - bool: True if the path is deleted or does not already exist, False otherwise.
    """

    # Check if the path is not specified
    if p == None:
        print("[INFO] No path specified")
        return False
    
    # Check if the path does not exist
    if not os.path.exists(p):
        print(f"[INFO] Path {p} does not exist")
        return True
    
    try:
        # Check if the path is empty and if the user wants to force it
        if os.listdir(p) != 0 and f == False:
            raise Exception()

        shutil.rmtree(p)
        print(f"[INFO] Path {p} deleted successfully")

        return True
    except Exception as e:
        # Handle potential errors during path creation
        print(f"[ERROR] Unable to delete path {p}: {e}")
        return False

def copy_path(p: str = None, d: str = None) -> bool:
    """
    Copy a directory to another path.

    Parameters:
    - p (str): The origin path.
    - d (str): The destination path.

    Returns:
    - bool: True if the path is copied, False otherwise.
    """

    # Check if the path or the destination is not specified
    if p == None or d == None:
        print("[INFO] No path or destination specified")
        return False

    # Check if the path exists
    if not os.path.exists(p):
        print(f"[INFO] Path {p} does not exist")
        return False

    try:
        # Ensure that the destination exists
        os.makedirs(d, exist_ok = True)

        # Copy every file
        for item in os.listdir(p):
            source_item = os.path.join(p, item)
            destination_item = os.path.join(d, item)

            # If it is a directory, call this function
            if os.path.isdir(source_item):
                copy_path(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)

        print(f"[INFO] Folder {p} successfully copied to {d}")
        return True
    except Exception as e:
        print(f"[ERROR] Folder {p} was not copied to {d}")
        return False

def delete_files(f: list[str] = None) -> bool:
    """Deletes one or more files.

    Parameters:
    - f (List[str]): A list of files to delete. If not specified, no files will be deleted.

    Returns:
    - bool: True if all files were successfully deleted, False otherwise.
    """

    # Check if the list is not specified
    if f == None:
        print("[INFO] No files specified")
        return False

    # Convert single string to list
    if type(f) == "str":
        f = [f]
    
    # Try to delete the files
    try:
        for file in f:
            if os.path.exists(file):
                os.remove(file)
                print(f"[INFO] File {file} deleted successfully")
            else:
                print(f"[INFO] File {file} does not exist")
    
        print("[INFO] Files deleted successfully")
        return True
    
    except Exception as e:
        print("[ERROR] Files were not deleted")
        return False
