import requests
import os
import bpy
from dotenv import load_dotenv
from .utilities.network_utilities import get_user_access_token


upload_endpoint = "/upload-assets/get-upload-urls"


def upload_single_frame_files():
    """ """

    upload_urls = get_upload_urls()

    if upload_urls:
        dir = os.path.dirname(__file__)
        render_properties = bpy.context.scene.render_properties

        if render_properties.beauty_pass_checkbox:
            beauty_path = os.path.join(dir, "renders", "beauty.png")
            beauty_url = upload_urls["beauty"]
            upload_file(beauty_url, beauty_path, True)

        if render_properties.normal_pass_checkbox:
            normal_path = os.path.join(dir, "renders", "normal.png")
            normal_url = upload_urls["normal"]
            upload_file(normal_url, normal_path, True)

        if render_properties.mask_pass_checkbox:
            mask_path = os.path.join(dir, "renders", "mask.png")
            mask_url = upload_urls["mask"]
            upload_file(mask_url, mask_path, True)

        # depth_path = os.path.join(dir, "renders", "depth.png")
        # depth_url = upload_urls["depth"]
        # upload_file(depth_url, depth_path)

        if render_properties.outline_pass_checkbox:
            outline_path = os.path.join(dir, "renders", "outline.png")
            outline_url = upload_urls["outline"]
            upload_file(outline_url, outline_path, True)


def upload_sequence_capture_files():
    """ """

    upload_urls = get_upload_urls()

    if upload_urls:
        dir = os.path.dirname(__file__)
        render_properties = bpy.context.scene.render_properties

        if render_properties.beauty_pass_checkbox:
            beauty_path = os.path.join(dir, "renders", "beauty_zip.zip")
            beauty_url = upload_urls["beauty_zip"]
            upload_file(beauty_url, beauty_path, False)

        if render_properties.mask_pass_checkbox:
            mask_path = os.path.join(dir, "renders", "mask_zip.zip")
            mask_url = upload_urls["mask_zip"]
            upload_file(mask_url, mask_path, False)


#
def get_upload_urls():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    url = "https://dev-accounts.playbook3d.com"  # os.getenv("BASE_ACCOUNTS_URL")

    access_token = get_user_access_token()

    response = requests.get(
        url=f"{url}{upload_endpoint}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return response.json() if response.status_code == 200 else None


#
def upload_file(signed_url: str, file_path: str, is_image: bool):
    with open(file_path, "rb") as file:
        response = requests.put(
            signed_url,
            data=file,
            headers={"Content-Type": "image/png" if is_image else "application/zip"},
        )
    print(f"Upload status: {response.status_code}")
