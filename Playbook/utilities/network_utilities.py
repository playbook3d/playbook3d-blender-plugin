import bpy
import json
import base64
import requests
from .file_utilities import get_env_value
from ..properties.team_properties import TeamProperties
from ..properties.workflow_properties import WorkflowProperties
from .. import __package__ as base_package

preferences = None


def get_user_info():
    """
    Returns the user's email, teams, and workflows.
    """

    try:
        teams_url = "https://accounts.playbook3d.com/teams/"
        workflows_url = "https://accounts.playbook3d.com/workflows"

        access_token = get_user_access_token()
        decoded_jwt = decode_jwt(access_token)
        decoded_json = json.loads(decoded_jwt)
        username = decoded_json["username"]

        url = get_env_value("USER_URL").replace("*", username)
        headers = {
            "authorization": access_token,
            "x-api-key": get_env_value("X_API_KEY"),
        }
        jwt_request = requests.get(url=url, headers=headers)
        request_data = jwt_request.json()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-API-KEY": get_env_value("X_API_KEY"),
        }
        teams_response = requests.get(url=teams_url, headers=headers)
        teams_response = json.loads(teams_response.text)
        workflows_response = requests.get(url=workflows_url, headers=headers)
        workflows_response = json.loads(workflows_response.text)

        return {
            "email": request_data["email"],
            "teams": [
                TeamProperties(team["id"], team["name"]) for team in teams_response
            ],
            "workflows": [
                WorkflowProperties(
                    workflow["id"], workflow["team_id"], workflow["name"]
                )
                for workflow in workflows_response
            ],
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_user_access_token():
    """
    Gets the user's access token based off the given API key.
    """

    try:
        alias_url = get_env_value("ALIAS_URL")
        api_key = get_api_key()
        jwt_request = requests.get(alias_url + api_key)

        return jwt_request.json()["access_token"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_api_key() -> str:
    """
    Returns the API key inputted by the user in the plugin's preferences.
    """

    global preferences

    if not preferences:
        addon = bpy.context.preferences.addons.get(base_package)
        if addon:
            preferences = addon.preferences
        else:
            print(f"Could not get user preferences!")

    return preferences.api_key


def get_run_id() -> str:
    """ """

    run_id_url = "https://api.playbook3d.com/get_run_id"
    request = requests.get(run_id_url)

    return request.json()["run_id"]


def decode_jwt(token: str):
    base64_url = token.split(".")[1]
    base64_str = base64_url.replace("-", "+").replace("_", "/")
    padded_base64_str = base64_str + "=" * (4 - len(base64_str) % 4)

    decoded_bytes = base64.b64decode(padded_base64_str)
    return decoded_bytes.decode("utf-8")
