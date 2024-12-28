import os
import json
import base64
import requests
from dotenv import load_dotenv
from ..properties.team_properties import TeamProperties
from ..properties.workflow_properties import WorkflowProperties
from .utilities import get_api_key


def get_user_info():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(dotenv_path=env_path)

    try:
        teams_url = "https://dev-accounts.playbook3d.com/teams/"
        workflows_url = "https://dev-accounts.playbook3d.com/workflows"

        access_token = get_user_access_token()
        decoded_jwt = decode_jwt(access_token)
        decoded_json = json.loads(decoded_jwt)
        username = decoded_json["username"]

        url = os.getenv("USER_URL").replace("*", username)
        headers = {"authorization": access_token, "x-api-key": os.getenv("X_API_KEY")}
        jwt_request = requests.get(url=url, headers=headers)
        request_data = jwt_request.json()

        # print(f"ACCESS TOKEN: {access_token}\n")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-API-KEY": os.getenv("BLENDER_X_API_KEY"),
        }
        teams_response = requests.get(url=teams_url, headers=headers)
        # print(f"TEAMS: {teams_response.text}\n")
        teams_response = json.loads(teams_response.text)
        workflows_response = requests.get(url=workflows_url, headers=headers)
        # print(f"WORKFLOWS: {workflows_response.text}")
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
    # Determine the path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    # Load the .env file
    load_dotenv(dotenv_path=env_path)

    try:
        alias_url = os.getenv("ALIAS_URL")
        api_key = get_api_key()
        jwt_request = requests.get(alias_url + api_key)

        return jwt_request.json()["access_token"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def decode_jwt(token: str):
    base64_url = token.split(".")[1]
    base64_str = base64_url.replace("-", "+").replace("_", "/")
    padded_base64_str = base64_str + "=" * (4 - len(base64_str) % 4)

    decoded_bytes = base64.b64decode(padded_base64_str)
    return decoded_bytes.decode("utf-8")
