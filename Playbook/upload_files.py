import requests
import bpy
from .utilities.network_utilities import get_user_access_token
from .utilities.file_utilities import get_filepath, get_env_value


upload_endpoint = "/upload-assets/get-upload-urls"


def upload_single_capture_files(run_id: str):
    """
    Upload the selected render pass images to the server.
    """

    upload_urls = get_upload_urls(run_id)

    if upload_urls:
        render_properties = bpy.context.scene.render_properties

        if render_properties.beauty_pass_checkbox:
            beauty_path = get_filepath("renders/beauty.png")
            beauty_url = upload_urls["beauty"]
            upload_file(beauty_url, beauty_path, True)

        if render_properties.normal_pass_checkbox:
            normal_path = get_filepath("renders/normal.png")
            normal_url = upload_urls["normal"]
            upload_file(normal_url, normal_path, True)

        if render_properties.mask_pass_checkbox:
            mask_path = get_filepath("renders/mask.png")
            mask_url = upload_urls["mask"]
            upload_file(mask_url, mask_path, True)

        if render_properties.outline_pass_checkbox:
            outline_path = get_filepath("renders/outline.png")
            outline_url = upload_urls["outline"]
            upload_file(outline_url, outline_path, True)


def upload_sequence_capture_files(run_id: str):
    """
    Upload the selected sequence capture render pass zip folders to the server.
    """

    upload_urls = get_upload_urls(run_id)

    if upload_urls:
        render_properties = bpy.context.scene.render_properties

        if render_properties.beauty_pass_checkbox:
            beauty_path = get_filepath("renders/beauty_zip.zip")
            beauty_url = upload_urls["beauty_zip"]
            upload_file(beauty_url, beauty_path, False)

        if render_properties.mask_pass_checkbox:
            mask_path = get_filepath("renders/mask_zip.zip")
            mask_url = upload_urls["mask_zip"]
            upload_file(mask_url, mask_path, False)


#
def get_upload_urls(run_id: str):
    url = get_env_value("BASE_ACCOUNTS_URL")

    access_token = get_user_access_token()

    response = requests.get(
        url=f"{url}{upload_endpoint}/{run_id}",
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
