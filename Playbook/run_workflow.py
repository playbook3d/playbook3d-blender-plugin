import os
import bpy
import json
import requests
from dotenv import load_dotenv
from .utilities.network_utilities import get_user_access_token


def run_workflow():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)

    try:
        url = os.getenv("WORKFLOW_URL")
        access_token = get_user_access_token()

        workflow_id = bpy.context.scene.user_properties.user_workflows_dropdown

        print(workflow_id)

        body = json.dumps({"id": workflow_id, "origin": 1, "inputs": {}})

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-API-KEY": os.getenv("BLENDER_X_API_KEY"),
        }

        response = requests.post(url=url, headers=headers, data=body)

        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
