import bpy
import json
import logging
import os
import traceback
import requests
import numpy as np
from comfydeploy import ComfyDeploy
from dotenv import load_dotenv
from ..render_status import RenderStatus
from ..utilities.utilities import get_scale_resolution_width, get_api_key
from ..workspace import open_render_window
from ..utilities.network_utilities import get_user_info
from ..utilities.secret_manager import BlenderSecretsManager

workflow_dict = {"RETEXTURE": 0, "STYLETRANSFER": 1}
base_model_dict = {"STABLE": 0, "FLUX": 1}
style_dict = {"PHOTOREAL": 0, "3DCARTOON": 1, "ANIME": 2}

result_counter = 0
status_counter = 0

RENDER_RESULT_CHECK_INTERVAL = 10
RENDER_STATUS_CHECK_INTERVAL = 5
RENDER_RESULT_ATTEMPT_LIMIT = 15
RENDER_STATUS_ATTEMPT_LIMIT = 30


#
def machine_id_status(machine_id: str):
    client = ComfyDeploy(bearer_auth="")

    client.machines.get_v1_machines_machine_id_(machine_id=machine_id)


class GlobalRenderSettings:
    def __init__(self, workflow: str, base_model: str, style: str, render_mode: int):
        self.workflow = workflow
        self.base_model = base_model
        self.style = style
        self.render_mode = render_mode


class MaskData:
    def __init__(self, color: str):
        self.color = color


class RetextureRenderSettings:
    def __init__(
        self,
        prompt: str,
        structure_strength: int,
        mask1: MaskData,
        mask2: MaskData,
        mask3: MaskData,
        mask4: MaskData,
        mask5: MaskData,
        mask6: MaskData,
        mask7: MaskData,
    ):
        self.prompt = prompt
        self.structure_strength = structure_strength
        self.mask1 = mask1
        self.mask2 = mask2
        self.mask3 = mask3
        self.mask4 = mask4
        self.mask5 = mask5
        self.mask6 = mask6
        self.mask7 = mask7


class StyleTransferRenderSettings:
    def __init__(self, prompt: str, style_transfer_strength: int):
        self.prompt = prompt
        self.style_transfer_strength = style_transfer_strength


def np_clamp(n: int, smallest: float, largest: float) -> int:
    return np.interp(n, [0, 100], [smallest, largest])


class ComfyDeployClient:
    def __init__(self):
        self.mask: bytes = b""
        self.depth: bytes = b""
        self.outline: bytes = b""
        self.beauty: bytes = b""
        self.normal: bytes = b""
        self.style_transfer: bytes = b""
        self.user_alias: str = ""
        self.user_token: str = ""
        self.run_id: str = ""

        # Determine the path to the .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

        # Load the .env file
        load_dotenv(dotenv_path=env_path)

        # Load env from secret manager
        BlenderSecretsManager.load_to_env()
        self.url = os.getenv("BASE_URL")

    def send_authorized_request(
        self, endpoint: str, data: any, files: any
    ) -> requests.Response:
        alias_url = os.getenv("ALIAS_URL")
        self.user_alias = get_api_key()
        jwt_request = requests.get(alias_url + self.user_alias)

        try:
            if jwt_request is not None:
                user_token = jwt_request.json()["access_token"]
                self.user_token = user_token
                render_result = requests.post(
                    self.url + endpoint,
                    data=data,
                    files=files,
                    headers={"Authorization": f"Bearer {user_token}"},
                )

                return render_result
        except requests.exceptions.RequestException as e:
            logging.error(f"Alias request failed {e}")
        except KeyError:
            logging.error("Access token not found in response")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Invalid JSON response {e}")

    def get_workflow_id(self, workflow: int, base_model: int, style: int) -> int:
        # Format is '{workflow}_{base_model}_{style}'
        ids = {
            # Generative Retexture
            "0_0_0": 0,
            "0_0_1": 1,
            "0_0_2": 2,
            "0_1_0": 3,
            "0_1_1": 4,
            "0_1_2": 5,
            # Style Transfer
            "1_0_0": 6,
            "1_0_1": 7,
            "1_0_2": 8,
            "1_1_0": 9,
            "1_1_1": 10,
            "1_1_2": 11,
        }

        key = f"{workflow}_{base_model}_{style}"
        if ids.get(key) is not None:
            return ids[key]

        return 0

    # Noting - in web repo, retexture and style transfer settings are combined into single RenderSettings. Should match
    async def run_workflow(
        self,
        global_settings: GlobalRenderSettings,
        retexture_settings: RetextureRenderSettings,
        style_transfer_settings: StyleTransferRenderSettings,
    ) -> str:
        if not self.mask or not self.depth or not self.outline:
            return "RENDER"

        try:
            global result_counter, status_counter
            result_counter = 0
            status_counter = 0

            # These are determined by UI selection:
            logging.info(f"Current workflow selection: {global_settings.workflow}")
            logging.info(f"Current base model: {global_settings.base_model}")
            logging.info(f"Current style: {global_settings.style}")

            clamped_retexture_depth = np_clamp(
                retexture_settings.structure_strength, 0.6, 1.0
            )
            clamped_retexture_outline = np_clamp(
                retexture_settings.structure_strength, 0.1, 0.3
            )
            clamped_style_transfer_depth = np_clamp(
                style_transfer_settings.style_transfer_strength, 0.6, 1.0
            )
            clamped_style_transfer_outline = np_clamp(
                style_transfer_settings.style_transfer_strength, 0.1, 0.3
            )

            clamped_style_transfer_strength = np_clamp(
                style_transfer_settings.style_transfer_strength, 0.0, 1.0
            )

            workflow_id = self.get_workflow_id(
                workflow_dict[global_settings.workflow],
                base_model_dict[global_settings.base_model],
                style_dict[global_settings.style],
            )
            logging.info(f"RUNNING WORKFLOW: {workflow_id}")

            match workflow_dict[global_settings.workflow]:
                # Generative Retexture
                case 0:
                    render_input = {
                        "is_blender_plugin": 1,
                        "workflow_id": workflow_id,
                        "scene_prompt": retexture_settings.prompt,
                        "structure_strength_depth": clamped_retexture_depth,
                        "structure_strength_outline": clamped_retexture_outline,
                    }
                    files = {
                        "beauty": self.beauty.decode("utf-8"),
                        "mask": self.mask.decode("utf-8"),
                        "depth": self.depth.decode("utf-8"),
                        "outline": self.outline.decode("utf-8"),
                    }
                    render_result = self.send_authorized_request(
                        "/generative-retexture", render_input, files
                    )

                # Style Transfer
                case 1:
                    render_input = {
                        "is_blender_plugin": 1,
                        "workflow_id": workflow_id,
                        "style_transfer_strength": clamped_style_transfer_strength,
                        "structure_strength_depth": clamped_style_transfer_depth,
                        "structure_strength_outline": clamped_style_transfer_outline,
                        "scene_prompt": style_transfer_settings.prompt,
                        "beauty": self.beauty,
                        "depth": self.depth,
                        "outline": self.outline,
                        "style_transfer_image": self.style_transfer,
                    }
                    files = {
                        "beauty": self.beauty.decode("utf-8"),
                        "depth": self.depth.decode("utf-8"),
                        "outline": self.outline.decode("utf-8"),
                        "style_transfer_image": self.style_transfer.decode("utf-8"),
                    }

                    render_result = self.send_authorized_request(
                        "/style-transfer", render_input, files
                    )

                # Workflow does not exist
                case _:
                    logging.error("Workflow input not valid")

            self.run_id = render_result.json()["run_id"]
            print(f"Current run id is {self.run_id}")

            bpy.app.timers.register(
                self.call_for_render_result, first_interval=RENDER_RESULT_CHECK_INTERVAL
            )
            bpy.app.timers.register(self.call_for_render_status, first_interval=0)

            return render_result.json()

        except Exception as e:
            print(f"Error occurred while running workflow: {e}")
            traceback.print_exc()
            return "RENDER"

    #
    def save_image(self, image: bytes, pass_type: str):
        match pass_type:
            case "mask":
                self.mask = image
            case "depth":
                self.depth = image
            case "outline":
                self.outline = image
            case "beauty":
                self.beauty = image
            case "normal":
                self.normal = image
            case "style_transfer":
                self.style_transfer = image

    #
    def get_render_result(self):
        try:
            if self.run_id is not None:
                run_uri = (
                    "https://dev-api.playbookengine.com"
                    + "/render-result?run_id="
                    + self.run_id
                )
                print(f"Current run is {run_uri}")
                rendered_img = requests.get(run_uri)
                return rendered_img
        except requests.exceptions.RequestException as e:
            logging.error(f"Result request failed {e}")
        except KeyError:
            logging.error("run_id not found in response")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Invalid JSON response {e}")

    #
    def call_for_render_result(self):
        print("starting to get render result")
        global result_counter
        result_counter += 1
        result = self.get_render_result()

        if result:
            rendered_image = result.text

            open_render_window(rendered_image)

            print(f"Image found!: {rendered_image}")
            return None

        if result_counter == RENDER_RESULT_ATTEMPT_LIMIT:
            return None

        return RENDER_RESULT_CHECK_INTERVAL

    #
    def get_render_status(self):
        try:
            if self.run_id is not None:
                run_uri = (
                    "https://dev-api.playbookengine.com"
                    + "/render-status?run_id="
                    + self.run_id
                )
                render_result = requests.get(run_uri)
                return render_result
        except requests.exceptions.RequestException as e:
            logging.error(f"Result request failed {e}")
        except KeyError:
            logging.error("run_id not found in response")
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Invalid JSON response {e}")

    #
    def call_for_render_status(self):
        if not RenderStatus.is_rendering:
            None

        global status_counter
        status_counter += 1
        status = self.get_render_status()

        if status:
            RenderStatus.set_render_status(status.content.decode("utf-8"))

            if status.content.decode("utf-8") == "success":
                user_info = get_user_info(get_api_key())
                RenderStatus.set_render_status("Ready")

                return None

        else:
            RenderStatus.set_render_status("Not started")

        if status_counter == RENDER_STATUS_ATTEMPT_LIMIT:
            return None

        return RENDER_STATUS_CHECK_INTERVAL
