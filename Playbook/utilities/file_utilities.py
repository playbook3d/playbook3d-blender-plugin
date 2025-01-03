import os
import shutil


#
def get_parent_filepath(filename, folder=""):
    dir = os.path.dirname(os.path.dirname(__file__))

    if not folder:
        return os.path.join(dir, filename)

    return os.path.join(dir, folder, filename)


#
def get_filepath(filename, folder=""):
    dir = os.path.dirname(__file__)

    if not folder:
        return os.path.join(dir, filename)

    return os.path.join(dir, folder, filename)


#
def is_valid_image_file(filepath: str) -> bool:
    valid_extensions = {".png", ".jpg", ".jpeg"}

    ext = filepath.lower().rsplit(".", 1)[-1]
    return f".{ext}" in valid_extensions


#
def clear_render_folder():
    dir = os.path.dirname(os.path.dirname(__file__))
    folder_path = os.path.join(dir, "renders")

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Failed to delete {folder_path}: {e}")
    else:
        print(f"File {folder_path} does not exist")


#
def create_zip_destination_folder(parent_dir, folder_name):
    dir = os.path.dirname(os.path.dirname(__file__))
    parent_path = os.path.join(dir, parent_dir)
    destination_path = os.path.join(parent_path, folder_name)

    os.makedirs(destination_path, exist_ok=True)
