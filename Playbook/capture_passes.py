import os
import bpy
import requests
from dotenv import load_dotenv
from .render_passes.render_passes import render_passes
from .utilities.network_utilities import get_user_access_token
from .utilities.file_utilities import clear_render_folder

upload_enpoint = "/upload-assets/get-upload-urls"


def capture_passes():
    clear_render_folder()

    render_passes()

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    url = "https://dev-accounts.playbook3d.com"  # os.getenv("BASE_ACCOUNTS_URL")

    upload_urls = get_upload_urls(url)

    if upload_urls:
        dir = os.path.dirname(__file__)
        render_properties = bpy.context.scene.render_properties

        if render_properties.beauty_pass_checkbox:
            beauty_path = os.path.join(dir, "renders", "beauty.png")
            beauty_url = upload_urls["beauty"]
            upload_file(beauty_url, beauty_path)

        if render_properties.normal_pass_checkbox:
            normal_path = os.path.join(dir, "renders", "normal.png")
            normal_url = upload_urls["normal"]
            upload_file(normal_url, normal_path)

        if render_properties.mask_pass_checkbox:
            mask_path = os.path.join(dir, "renders", "mask.png")
            mask_url = upload_urls["mask"]
            upload_file(mask_url, mask_path)

        # depth_path = os.path.join(dir, "renders", "depth.png")
        # depth_url = upload_urls["depth"]
        # upload_file(depth_url, depth_path)

        if render_properties.outline_pass_checkbox:
            outline_path = os.path.join(dir, "renders", "outline.png")
            outline_url = upload_urls["outline"]
            upload_file(outline_url, outline_path)

    return


#
def get_upload_urls(url):
    access_token = get_user_access_token()

    response = requests.get(
        url=f"{url}{upload_enpoint}",
        headers={"Authorization": f"Bearer {access_token}"},
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
