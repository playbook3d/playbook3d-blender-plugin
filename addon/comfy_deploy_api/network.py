import json
import logging
import os
import requests
import numpy as np
from websockets.sync.client import connect
from comfydeploy import ComfyDeploy


def machine_id_status(machine_id: str):
    client = ComfyDeploy(bearer_auth="")

    client.machines.get_v1_machines_machine_id_(machine_id=machine_id)

    #  /run-workflow


class GeneralSettings:
    def __init__(self, workflow: int, model: int, style: int, render_mode: int):
        self.workflow = workflow
        self.model = model
        self.style = style
        self.renderMode = render_mode


class MaskSettings:
    def __init__(self, prompt: str, color: str):
        self.mask_prompt = prompt
        self.color = color


class RetextureSettings:
    def __init__(self, prompt: str, structure_strength: int):
        self.prompt = prompt
        self.structure_strength = structure_strength


class StyleTransferSettings:
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

        self.url = os.getenv("BASE_URL")

    async def run_retexture_workflow(
        self,
        mask_settings1: MaskSettings,
        mask_settings2: MaskSettings,
        mask_settings3: MaskSettings,
        mask_settings4: MaskSettings,
        retexture_settings: RetextureSettings,
    ) -> str:
        files = {
            "prompt": retexture_settings.prompt,
            "prompt a": mask_settings1.mask_prompt,
            "prompt b": mask_settings2.mask_prompt,
            "prompt c": mask_settings3.mask_prompt,
            "prompt d": mask_settings4.mask_prompt,
            "mask": self.mask,
            "depth": self.depth,
            "outline": self.outline,
        }

        render_result = requests.post(self.url + "/upload-images", files=files)
        if render_result.status_code != 200:
            return render_result.json()

    async def run_workflow(
        self,
        general_settings: GeneralSettings,
        mask_settings1: MaskSettings,
        mask_settings2: MaskSettings,
        mask_settings3: MaskSettings,
        mask_settings4: MaskSettings,
        mask_settings5: MaskSettings,
        mask_settings6: MaskSettings,
        mask_settings7: MaskSettings,
        retexture_settings: RetextureSettings,
        style_transfer_settings: StyleTransferSettings,
    ) -> str:

        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {retexture_settings.prompt}")

            clamped_retexture_depth = np_clamp(retexture_settings.structure_strength, 0.6, 1.0)
            clamped_retexture_outline = np_clamp(retexture_settings.structure_strength, 0.1, 0.3)
            clamped_style_transfer_strength = np_clamp(style_transfer_settings.style_transfer_strength, 0.0, 1.0)
            retexture_input = {
                "width": 512,
                "height": 512,
                "scene_prompt": retexture_settings.prompt,
                "structure_strength_depth": clamped_retexture_depth,
                "structure_strength_outline": clamped_retexture_outline,
                "mask_prompt_1": mask_settings1.mask_prompt,
                "mask_prompt_2": mask_settings2.mask_prompt,
                "mask_prompt_3": mask_settings3.mask_prompt,
                "mask_prompt_4": mask_settings4.mask_prompt,
                "mask_prompt_5": mask_settings5.mask_prompt,
                "mask_prompt_6": mask_settings6.mask_prompt,
                "mask_prompt_7": mask_settings7.mask_prompt,
                "mask": self.mask,
                "depth": self.depth,
                "outline": self.outline
            }

            style_transfer_input = {
                "strength": clamped_style_transfer_strength,
                "width": 512,
                "height": 512,
                "beauty": self.beauty,
                "depth": self.depth,
                "outline": self.outline,
                "style_transfer_image": self.style_transfer
            }

            match general_settings.workflow:
                case 0:
                    #  SD Retexture
                    render_result = requests.post(self.url + "/retexture", files=retexture_input)
                    if render_result.status_code != 200:
                        return render_result.json()

                case 1:
                    #  FLUX Retexture
                    render_result = requests.post(self.url + "/flux-retexture", files=retexture_input)
                    if render_result.status_code != 200:
                        return render_result.json()

                case 2:
                    #  SD Style Transfer
                    render_result = requests.post(self.url + "/style-transfer", files=style_transfer_input)
                    if render_result.status_code != 200:
                        return render_result.json()

                case 3:
                    #  FLUX Style Transfer
                    render_result = requests.post(self.url + "/flux-style-transfer", files=style_transfer_input)
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
