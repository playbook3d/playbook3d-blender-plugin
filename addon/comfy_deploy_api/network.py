import json
import logging
import os
import requests
import numpy as np
from websockets.sync.client import connect
from comfydeploy import ComfyDeploy
from dotenv import load_dotenv


def machine_id_status(machine_id: str):
    client = ComfyDeploy(bearer_auth="")

    client.machines.get_v1_machines_machine_id_(machine_id=machine_id)

    #  /run-workflow


class GlobalRenderSettings:
    def __init__(self, workflow: int, render_mode: int):
        self.workflow = workflow
        self.renderMode = render_mode


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
    def __init__(self, strength: int):
        self.style_transfer_strength = strength


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

    async def run_retexture_workflow(
        self,
        retexture_settings: RetextureRenderSettings,
    ) -> str:
        print(f"Prompt: {retexture_settings.prompt}")
        files = {
            "prompt": retexture_settings.prompt,
            "prompt a": retexture_settings.mask1.mask_prompt,
            "prompt b": retexture_settings.mask2.mask_prompt,
            "prompt c": retexture_settings.mask3.mask_prompt,
            "prompt d": retexture_settings.mask4.mask_prompt,
            "mask": self.mask,
            "depth": self.depth,
            "outline": self.outline,
        }

        render_result = requests.post(self.url + "/upload-images", files=files)
        if render_result.status_code != 200:
            return render_result.json()

    async def run_workflow(
        self,
        global_settings: GlobalRenderSettings,
        retexture_settings: RetextureRenderSettings,
        style_transfer_settings: StyleTransferRenderSettings,
    ) -> str:

        if self.mask and self.depth and self.outline:
            logging.info(f"Starting workflow for prompt: {retexture_settings.prompt}")

            clamped_retexture_depth = np_clamp(
                retexture_settings.structure_strength, 0.6, 1.0
            )
            clamped_retexture_outline = np_clamp(
                retexture_settings.structure_strength, 0.1, 0.3
            )
            clamped_style_transfer_strength = np_clamp(
                style_transfer_settings.style_transfer_strength, 0.0, 1.0
            )
            retexture_input = {
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

            style_transfer_input = {
                "strength": clamped_style_transfer_strength,
                "width": 512,
                "height": 512,
                "beauty": self.beauty,
                "depth": self.depth,
                "outline": self.outline,
                "style_transfer_image": self.style_transfer,
            }

            match global_settings.workflow:
                case 0:
                    #  SD Retexture
                    render_result = requests.post(
                        self.url + "/retexture", files=retexture_input
                    )
                    if render_result.status_code != 200:
                        return render_result.json()

                case 1:
                    #  FLUX Retexture
                    render_result = requests.post(
                        self.url + "/flux-retexture", files=retexture_input
                    )
                    if render_result.status_code != 200:
                        return render_result.json()

                case 2:
                    #  SD Style Transfer
                    render_result = requests.post(
                        self.url + "/style-transfer", files=style_transfer_input
                    )
                    if render_result.status_code != 200:
                        return render_result.json()

                case 3:
                    #  FLUX Style Transfer
                    render_result = requests.post(
                        self.url + "/flux-style-transfer", files=style_transfer_input
                    )
                    if render_result.status_code != 200:
                        return render_result.json()

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
