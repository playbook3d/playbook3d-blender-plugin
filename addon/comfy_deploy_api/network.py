import json
import logging
import os
import requests
import numpy as np
from websockets.sync.client import connect
from comfydeploy import ComfyDeploy
from dotenv import load_dotenv

workflow_dict = {"RETEXTURE": 0, "STYLETRANSFER": 1}
base_model_dict = {"SDXL": 0, "FLUX": 1}
style_dict = {"PHOTOREAL": 0, "3DCARTOON": 1, "ANIME": 2}


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
    def __init__(self, prompt: str, color: str):
        self.mask_prompt = prompt
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
    def __init__(
        self, prompt: str, structure_strength: int, style_transfer_strength: int
    ):
        self.prompt = prompt
        self.structure_strength = structure_strength
        self.style_transfer_strength = style_transfer_strength


def np_clamp(n: int, smallest: float, largest: float) -> int:
    return np.interp(n, [0, 100], [smallest, largest])


class ComfyDeployClient:
    def __init__(self):
        self.mask: bytes = b""
        self.depth: bytes = b""
        self.outline: bytes = b""
        self.beauty: bytes = b""
        self.style_transfer: bytes = b""

        # Determine the path to the .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

        # Load the .env file
        load_dotenv(dotenv_path=env_path)

        self.url = os.getenv("BASE_URL")

    def get_workflow_id(self, workflow: int, base_model: int, style: int) -> int:
        # Format is '{workflow}_{baseModel}_{style}'
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

        if self.mask and self.depth and self.outline:
            # These are determined by UI selection:
            logging.info(f"Current workflow selection: {global_settings.workflow}")
            print(f"Current workflow selection: {global_settings.workflow}")
            logging.info(f"Current base model: {global_settings.base_model}")
            print(f"Current base model: {global_settings.base_model}")
            logging.info(f"Current style: {global_settings.style}")
            print(f"Current style: {global_settings.style}")

            clamped_retexture_depth = np_clamp(
                retexture_settings.structure_strength, 0.6, 1.0
            )
            clamped_retexture_outline = np_clamp(
                retexture_settings.structure_strength, 0.1, 0.3
            )
            clamped_style_transfer_depth = np_clamp(
                style_transfer_settings.structure_strength, 0.6, 1.0
            )
            clamped_style_transfer_outline = np_clamp(
                style_transfer_settings.structure_strength, 0.1, 0.3
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
            print(f"RUNNING WORKFLOW: {workflow_id}")

            temp = 0
            match temp:
                # Generative Retexture
                case 0:
                    input = {
                        "workflow_id": 0,
                        "width": 512,
                        "height": 512,
                        "scene_prompt": retexture_settings.prompt,
                        "structure_strength_depth": clamped_retexture_depth,
                        "structure_strength_outline": clamped_retexture_outline,
                        "mask_prompt_1": retexture_settings.mask1.mask_prompt,
                        "mask_prompt_2": retexture_settings.mask2.mask_prompt,
                        "mask_prompt_3": retexture_settings.mask3.mask_prompt,
                        "mask_prompt_4": retexture_settings.mask4.mask_prompt,
                        "mask_prompt_5": retexture_settings.mask5.mask_prompt,
                        "mask_prompt_6": retexture_settings.mask6.mask_prompt,
                        "mask_prompt_7": retexture_settings.mask7.mask_prompt,
                        "mask": self.mask,
                        "depth": self.depth,
                        "outline": self.outline,
                    }
                    render_result = requests.post(
                        self.url + "/generative-retexture", data=input
                    )
                    return render_result.json()

                # Style Transfer
                case 1:
                    input = {
                        "workflow_id": workflow_id,
                        "width": 512,
                        "height": 512,
                        "style_transfer_strength": clamped_style_transfer_strength,
                        "structure_strength_depth": clamped_style_transfer_depth,
                        "structure_strength_outline": clamped_style_transfer_outline,
                        "scene_prompt": style_transfer_settings.prompt,
                        "beauty": self.beauty,
                        "depth": self.depth,
                        "outline": self.outline,
                        "style_transfer_image": self.style_transfer,
                    }
                    render_result = requests.post(
                        self.url + "/style-transfer", files=input
                    )
                    if render_result.status_code != 200:
                        return render_result.json()
                case _:
                    logging.error("Workflow input not valid")

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
            case "style_transfer":
                self.style_transfer = image


class PlaybookWebsocket:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.websocket = None

    async def websocket_message(self) -> str:
        try:
            async with connect(self.base_url) as websocket:
                self.websocket = websocket

                while True:
                    message = await websocket.recv()
                    try:
                        data = json.loads(message)

                        if data.get("status") == "success":
                            extracted_data = data.get["data"]
                            image_url = extracted_data.outputs[0].data.images[0].url
                            return image_url

                    except json.JSONDecodeError:
                        print("Error while parsing response from server", message)

        except Exception as exception:
            print(f"Error while parsing response from server: {exception}")
