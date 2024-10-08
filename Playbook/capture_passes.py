import os
import bpy
import requests
from dotenv import load_dotenv
from .render_passes.render_passes import render_passes
from .utilities.utilities import get_api_key


def capture_passes():

    # Render passes failed
    if not render_passes():
        return

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    url = os.getenv("BASE_ACCOUNTS_URL")

    upload_urls = get_upload_urls(url)

    if upload_urls:
        print(upload_urls)

    return


#
def get_upload_urls(url):
    alias_url = os.getenv("ALIAS_URL")
    user_alias = get_api_key()
    jwt_request = requests.get(alias_url + user_alias)
    if jwt_request is not None:
        user_token = jwt_request.json()["access_token"]

    response = requests.get(
        url=f"{url}/upload-assets/get-upload-urls",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    return response.json() if response.status_code == 200 else None


#
def get_download_urls(url, headers):
    response = requests.get(
        url=f"{url}/upload-assets/get-download-urls", headers=headers
    )
    return response.json() if response.status_code == 200 else None


#
def upload_file(signed_url, file_path):
    with open(file_path, "rb") as file:
        response = requests.put(
            signed_url, data=file, headers={"Content-Type": "image/png"}
        )
    print(f"Upload status: {response.status_code}")


#
def download_file(signed_url, save_path):
    response = requests.get(signed_url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded to {save_path}")
    else:
        print(f"Download failed: {response.status_code}")


# Returns True if an error occurs while attempting to render the image.
def error_exists_in_capture_passes(scene) -> bool:
    # [workflow, condition for error message]
    workflow_checks = {
        "APIKEY": bpy.context.preferences.addons.get("Playbook").preferences.api_key
        == "",
    }

    # [workflow, error message]
    messages = {
        "APIKEY": "Copy your API key from the Playbook web editor.",
    }

    for key, val in workflow_checks.items():
        if val:
            scene.error_message = messages[key]
            return True

    scene.error_message = ""
    return False
