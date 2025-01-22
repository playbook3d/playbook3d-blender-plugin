import os
import shutil
import zipfile
from dotenv import load_dotenv


#
def get_filepath(filename: str) -> str:
    """
    Returns the filepath of the given filename relative to the
    root directory.
    """

    dir = os.path.dirname(os.path.dirname(__file__))

    return os.path.join(dir, filename)


def get_env_value(key: str) -> str:
    """
    Returns the value of the .env file of the given key.
    """

    # Determine the path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    load_dotenv(dotenv_path=env_path)

    return os.getenv(key)


#
def is_valid_image_file(filepath: str) -> bool:
    """
    Returns true if the given filepath has a valid image type.
    i.e. ".png", ".jpg", ".jpeg"
    """

    valid_extensions = {".png", ".jpg", ".jpeg"}

    ext = filepath.lower().rsplit(".", 1)[-1]
    return f".{ext}" in valid_extensions


#
def clear_folder_contents(folder_name: str):
    """
    Clear the contents of the given folder.
    """

    dir = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(dir, folder_name)

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Failed to delete {folder_path}: {e}")
    else:
        print(f"File {folder_path} does not exist")


#
def create_folder(parent_dir: str, folder_name: str):
    """
    Create a folder with the given name at the given directory.
    """

    dir = os.path.dirname(os.path.dirname(__file__))
    parent_path = os.path.join(dir, parent_dir)
    destination_path = os.path.join(parent_path, folder_name)

    os.makedirs(destination_path, exist_ok=True)


#
def zip_folder(source_folder: str):
    """
    Zip up the contents of the given folder. Replaces the source folder
    with the zipped folder.
    """

    with zipfile.ZipFile(f"{source_folder}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, start=source_folder)
                zipf.write(filepath, relpath)

    shutil.rmtree(source_folder)
