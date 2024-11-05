import os
import json
import base64
import requests
from dotenv import load_dotenv


def get_user_info(api_key: str):
    # Determine the path to the .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    # Load the .env file
    load_dotenv(dotenv_path=env_path)

    try:
        alias_url = os.getenv("ALIAS_URL")
        jwt_request = requests.get(alias_url + api_key)

        access_token = jwt_request.json()["access_token"]
        decoded_jwt = decode_jwt(access_token)

        decoded_json = json.loads(decoded_jwt)
        username = decoded_json["username"]

        url = os.getenv("USER_URL").replace("*", username)
        print(url)
        headers = {"authorization": access_token, "x-api-key": os.getenv("X_API_KEY")}
        jwt_request = requests.get(url=url, headers=headers)
        request_data = jwt_request.json()

        return {
            "email": request_data["email"],
            "credits": request_data["users_tier"]["credits"],
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def decode_jwt(token: str):
    base64_url = token.split(".")[1]
    base64_str = base64_url.replace("-", "+").replace("_", "/")
    padded_base64_str = base64_str + "=" * (4 - len(base64_str) % 4)

    decoded_bytes = base64.b64decode(padded_base64_str)
    return decoded_bytes.decode("utf-8")
