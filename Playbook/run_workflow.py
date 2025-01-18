import bpy
import json
import requests
from .capture_passes import capture_passes
from .upload_files import upload_single_capture_files, upload_sequence_capture_files
from .properties.user_properties import get_team_id_of_workflow
from .utilities.network_utilities import get_user_access_token
from .utilities.file_utilities import get_env_value
from .utilities.utilities import does_plugin_error_exists


def run_single_image_capture():
    """
    Run the given workflow after capturing single images of the
    selected passes
    """

    if does_plugin_error_exists():
        return

    capture_passes(False)

    run_id = run_workflow()

    upload_single_capture_files(run_id)


def run_workflow():
    """
    Requests the server to start running the selected workflow.
    """

    try:
        url = get_env_value("WORKFLOW_URL")
        access_token = get_user_access_token()
        workflow_id = bpy.context.scene.user_properties.user_workflows_dropdown
        url = url + f"/{get_team_id_of_workflow(workflow_id)}"

        print(f"Workflow URL: {url}")
        print(f"Workflow ID: {workflow_id}")

        body = json.dumps({"id": workflow_id, "origin": 1, "inputs": {}})

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-API-KEY": get_env_value("BLENDER_X_API_KEY"),
        }

        response = requests.post(url=url, headers=headers, data=body)

        print(f"Run Workflow Response: {response.text}")

        display_submission_message()

        return response.json()["run_id"]

    except Exception as e:
        print(f"Status code: {response.status_code}")
        print(f"An error occurred while attempting to run the workflow: {e}")
        return None


def display_submission_message():
    bpy.context.scene.status_message = "Workflow Run Submitted."

    # Remove submission message after 10 seconds
    bpy.app.timers.register(remove_submission_message, first_interval=10)


def remove_submission_message():
    bpy.context.scene.status_message = ""

    return None
