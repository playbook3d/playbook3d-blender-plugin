import json
from typing import Sequence
import logging
import os
import requests
import datetime
import numpy as np
from websockets.sync.client import connect
import asyncio


class GeneralSettings:
    def __init__(self, model: int, bias: int, prompt: str, strength: int):
        self.model = model
        self.bias = bias
        self.scene_prompt = prompt
        self.structure_strength = strength


class MaskSettings:
    def __init__(self, prompt: str, color: str):
        self.mask_prompt = prompt
        self.color = color


class StyleTransferSettings:
    def __init__(self, strength: int):
        self.style_transfer_strength = strength


class RelightSettings:
    def __init__(self, color: str, prompt: str, angle: int):
        self.relight_color = color
        self.relight_prompt = prompt
        self.relight_angle = angle


class UpscaleSettings:
    def __init__(self, model: int, value: int, creativity: int, prompt: str):
        self.upscale_model = model
        self.upscale_value = value
        self.upscale_creativity = creativity
        self.upscale_prompt = prompt


class ComfyDeployImage:
    url: str
    type: str
    filename: str
    subfolder: str

    def __init__(self, url: str, type: str, filename: str, subfolder: str):
        self.url = url
        self.type = type
        self.filename = filename
        self.subfolder = subfolder


class OutputData:
    images: Sequence[ComfyDeployImage]

    def __init__(self, images: Sequence[ComfyDeployImage]):
        self.images = images


class ComfyDeployOutput:
    id: str
    run_id: str
    data: OutputData
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: str,
        run_id: str,
        data: OutputData,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.run_id = run_id
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at


class ComfyDeployResultData:
    status: str
    run_id: str
    outputs: Sequence[ComfyDeployOutput]

    def __init__(self, status: str, run_id: str, outputs: Sequence[ComfyDeployOutput]):
        self.status = status
        self.run_id = run_id
        self.outputs = outputs


class ComfyDeployResult:
    status: str
    progress: int
    data: ComfyDeployResultData

    def __init__(self, status: str, progress: int, data: ComfyDeployResultData):
        self.status = status
        self.progress = progress
        self.data = data


def np_clamp(n: int, smallest: float, largest: float) -> int:
    return np.interp(n, [0, 100], [smallest, largest])


class ComfyDeployClient:
    def __init__(self):
        self.mask: bytes = b""
        self.depth: bytes = b""
        self.outline: bytes = b""
        self.normal: bytes = b""
        self.beauty: bytes = b""
        self.style_transfer: bytes = b""
        self.relight: bytes = b""
        self.internal_pass: str = ""

        self.url = os.getenv("BASE_URL")

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
        style_transfer_settings: StyleTransferSettings,
        relight_settings: RelightSettings,
        upscale_settings: UpscaleSettings,
        render_mode: int,
        retexture_enabled: bool,
        style_transfer_enabled: bool,
        relight_enabled: bool,
        upscale_enabled: bool,
    ) -> str:
        clamped_structure_strength = np_clamp(general_settings.structure_strength, 0.6, 1)

        internal_model = ""
        match general_settings.model:
            case 0:
                internal_model = "juggernaut_reborn.safetensors"
            case 1:
                internal_model = "disneyPixarCartoon_v10.safetensors"
            case 2:
                internal_model = "flat2DAnimerge_v45Sharp.safetensors"

        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {general_settings.scene_prompt} "
            )
            files = {
                "model": internal_model,
                "scenePrompt": general_settings.scene_prompt,
                "structureStrength": clamped_structure_strength,
                "mask1": mask_settings1.mask_prompt,
                "mask2": mask_settings2.mask_prompt,
                "mask3": mask_settings3.mask_prompt,
                "mask4": mask_settings4.mask_prompt,
                "mask5": mask_settings5.mask_prompt,
                "mask6": mask_settings6.mask_prompt,
                "mask7": mask_settings7.mask_prompt,
                "beauty": self.beauty,
                "mask": self.mask,
                "depth": self.depth,
                "outline": self.outline,
            }

            run_result = requests.post(self.url + "/upload-images", data=files)

            if retexture_enabled:
                self.run_retexture(general_settings.scene_prompt)

            if style_transfer_enabled:
                self.run_style_transfer(style_transfer_settings)

            if relight_enabled:
                self.run_relight(relight_settings)

            if upscale_enabled:
                self.run_upscale(upscale_settings)

            if run_result is not None:
                return run_result.json()
            else:
                logging.error(f"Error running workflow: {run_result}")

    #
    def run_retexture(self, prompt: str):
        # TODO: retexture
        if prompt:
            retexture_result = requests.post(
                self.url + "/retexture", json={"prompt": prompt}
            )
            if retexture_result is not None:
                self.internal_pass = retexture_result.json()["internal_pass"]

    #
    def run_style_transfer(self, style_transfer_settings: StyleTransferSettings):
        # TODO: style transfer
        clamped_style_transfer_strength = np_clamp(style_transfer_settings.style_transfer_strength, 0.3, 1)
        if clamped_style_transfer_strength:
            files = {
                "strength": clamped_style_transfer_strength,
                "input_image": self.internal_pass
            }
            style_transfer_result = requests.post(self.url + "/style-transfer", files=files)
            if style_transfer_result is not None:
                self.internal_pass = style_transfer_result.json()["internal_pass"]

    #
    def run_relight(
        self,
        relight_settings: RelightSettings
    ):
        # TODO: relight
        color = relight_settings.relight_color
        prompt = relight_settings.relight_prompt
        angle = relight_settings.relight_angle
        if color and prompt and angle:
            files = {
                "color": color,
                "prompt": prompt,
                "angle": angle,
                "input_image": self.internal_pass
            }
            relight_result = requests.post(self.url + "/relight", files=files)
            if relight_result is not None:
                self.internal_pass = relight_result.json()["internal_pass"]

    #
    def run_upscale(self, upscale_settings: UpscaleSettings):
        # TODO: upscale
        model = upscale_settings.upscale_model
        value = upscale_settings.upscale_value
        clamped_upscale_creativity = np_clamp(upscale_settings.upscale_creativity, 0.3, 0.75)
        prompt = upscale_settings.upscale_prompt

        if model and value and clamped_upscale_creativity and prompt:
            files = {
                "model": model,
                "value": value,
                "creativity": clamped_upscale_creativity,
                "prompt": prompt,
                "input_image": self.internal_pass
            }
            upscale_result = requests.post(self.url + "/upscale", files=files)
            if upscale_result is not None:
                self.internal_pass = upscale_result.json()["internal_pass"]

    #
    def save_image(self, image: bytes, pass_type: str):
        match pass_type:
            case "mask":
                self.mask = image
            case "depth":
                self.depth = image
            case "outline":
                self.outline = image
            case "normal":
                self.normal = image
            case "beauty":
                self.beauty = image
            case "style_transfer":
                self.style_transfer = image
            case "relight":
                self.relight = image

    #
    def save_internal_image(self, image_url: str):
        self.internal_pass = image_url


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

