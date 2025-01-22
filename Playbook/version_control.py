import os
import requests
import shutil
import zipfile
from packaging import version
from .utilities.utilities import show_message_box
from .utilities.file_utilities import get_env_value


class PlaybookVersionControl:

    can_update = False
    version_control_label = ""

    @classmethod
    def check_if_version_up_to_date(cls, current_version):
        url = get_env_value("LATEST_VERSION_URL")
        response = requests.get(url)

        if response.status_code == 200:
            latest_version = version.parse(response.text)

            current_version = version.parse(
                f"{str(current_version[0])}.{str(current_version[1])}.{str(current_version[2])}"
            )

            print(f"Current version of Playbook: {current_version}")

            if latest_version > current_version:
                cls.can_update = True
                cls.version_control_label = "You can update to our latest version."
                print(f"You can update your Playbook to {latest_version}")
            else:
                cls.version_control_label = "You have the latest version of Playbook."

        return

    @classmethod
    def update_addon(cls):
        zip_path = download_latest_zip()

        if zip_path:
            extract_zip(zip_path)


def download_latest_zip():
    url = get_env_value("LATEST_VERSION_ZIP_URL")
    download_response = requests.get(url)

    if download_response.status_code != 200:
        return None

    download_url = download_response.text
    latest_zip = requests.get(download_url)

    if latest_zip.status_code != 200:
        return None

    addons_path = os.path.dirname(os.path.dirname(__file__))
    zip_path = os.path.join(addons_path, "latest_version.zip")

    with open(zip_path, "wb") as zip:
        zip.write(latest_zip.content)

    return zip_path


def extract_zip(zip_path):
    try:
        addons_path = os.path.dirname(os.path.dirname(__file__))
        extracted_path = os.path.join(addons_path, "extracted_zip")

        with zipfile.ZipFile(zip_path, "r") as zip:
            zip.extractall(extracted_path)

        playbook_path = os.path.join(extracted_path, "Playbook")
        destination_path = os.path.join(addons_path, "Playbook")

        if os.path.exists(playbook_path):
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)

            shutil.move(playbook_path, destination_path)

            shutil.rmtree(extracted_path)
            os.unlink(zip_path)

            message_lines = ["Please restart Blender."]
            show_message_box(message_lines, "Update Sucessful!")

            PlaybookVersionControl.version_control_label = (
                "Update was successful! Please restart Blender."
            )
            PlaybookVersionControl.can_update = False

    except Exception as e:
        print(e)
