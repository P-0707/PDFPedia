import os
import json
from plyer import filechooser

def load_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
    return {}

def save_data(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def get_internal_storage_path(filename):
    """
    Returns the path to the internal storage directory.
    
    Args:
        filename (str): The name of the file to store in the internal storage.
        
    Returns:
        str: Full path to the file in the internal storage.
    """
    #return os.path.join(os.path.expanduser("~"), filename)  # Adjust this for mobile internal storage path
    return os.path.join("C:\\Users\\pavani\\Desktop", filename)

def open_file_dialog():
    """
    Opens a file chooser dialog to select a PDF file.
    
    Returns:
        list: List of selected file paths.
    """
    return filechooser.open_file(title="Pick a PDF file", filters=[("PDF Files", "*.pdf")])
