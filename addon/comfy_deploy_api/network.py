from typing import Sequence, Optional
import logging
import os
import requests
import datetime
import numpy as np

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

    def __init__(self, id: str, run_id: str, data: OutputData, created_at: datetime, updated_at: datetime):
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

    async def run_workflow(
        self,
            retexture_model: int,  # 0 Juggernaut, 1 pixar, 2 anime
            retexture_bias: int,
            retexture_scene_prompt: str,
            retexture_structure_strength: int,  # 0-100 clamp Control nets depth (0.6 - 1), canny (0.1 - 0.3)
            retexture_prompt_1: str,
            retexture_prompt_2: str,
            retexture_prompt_3: str,
            retexture_prompt_4: str,
            retexture_prompt_5: str,
            retexture_prompt_6: str,
            retexture_prompt_7: str,
            style_transfer_strength: int,  # 0-100 (0.3 - 1) ipAdapter
            relight_color: str,
            relight_prompt: str,
            relight_angle: int,
            upscale_model: int,
            upscale_value: int,
            upscale_creativity: int,  # 0 - 100 (0.3 - 0.75) denoise
            upscale_prompt: str,
            render_mode: int,  # 0 render image / 1 render video
            retexture_enabled: bool,
            style_transfer_enabled: bool,
            relight_enabled: bool,
            upscale_enabled: bool,
    ) -> str:
        clamped_structure_strength = np_clamp(retexture_structure_strength, 0.6, 1)
        clamped_style_transfer_strength = np_clamp(style_transfer_strength, 0.3, 1)
        clamped_upscale_creativity = np_clamp(upscale_creativity, 0.3, 0.75)

        internal_model = ""
        match retexture_model:
            case 0:
                internal_model = "juggernaut_reborn.safetensors"
            case 1:
                internal_model = "disneyPixarCartoon_v10.safetensors"
            case 2:
                internal_model = "flat2DAnimerge_v45Sharp.safetensors"

        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {retexture_scene_prompt} "
                f"with detailed prompt {retexture_prompt_1}, {retexture_prompt_2}, {retexture_prompt_3}, {retexture_prompt_4}"
            )
            files = {
                "model": internal_model,
                "prompt": retexture_scene_prompt,
                "prompt_a": retexture_prompt_1,
                "prompt_b": retexture_prompt_2,
                "prompt_c": retexture_prompt_3,
                "prompt_d": retexture_prompt_4,
                "mask": self.mask,
                "depth": self.depth,
                "outline": self.outline,
            }
            run_result = requests.post(os.getenv("BASE_URL") + "/upload-images", files=files)

            if style_transfer_enabled:
                self.run_style_transfer(clamped_style_transfer_strength)

            if relight_enabled:
                self.run_relight(relight_color, relight_prompt, relight_angle)

            if upscale_enabled:
                self.run_upscale(upscale_prompt, upscale_value, clamped_upscale_creativity)

            if run_result is not None:
                return run_result.json()
            else:
                logging.error(f"Error running workflow: {run_result}")

    def run_relight(self, color: str, prompt: str, angle: int):
        # TODO: connect to new endpoint for relight
        if color and prompt and angle:
            files = {
                "relight_color": color,
                "relight_prompt": prompt,
                "relight_angle": angle,
                "input_image": self.internal_pass
            }
            relight_result = requests.post(os.getenv("BASE_URL") + "/relight", files=files)
            if relight_result is not None:
                self.internal_pass = relight_result.json()["internal_pass"]

    def run_upscale(self, model: str, prompt: str, value: int, creativity: int):
        # TODO: connect to new endpoint for upscale(flux)
        if value and creativity:
            files = {
                "model": model,
                "prompt": prompt,
                "upscale_value": value,
                "upscale_creativity": creativity,
                "input_image": self.internal_pass
            }
            upscale_result = requests.post(os.getenv("BASE_URL") + "/upscale", files=files)
            if upscale_result is not None:
                self.internal_pass = upscale_result.json()["internal_pass"]

    def run_style_transfer(self, strength: int):
        # TODO: style transfer
        if strength:
            files = {
                "style_transfer_strength": strength,
                "input_image": self.internal_pass
            }
            style_transfer_result = requests.post(os.getenv("BASE_URL") + "/style-transfer",
                                                  files=files)
            if style_transfer_result is not None:
                self.internal_pass = style_transfer_result.json()["internal_pass"]

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

    def save_internal_image(self, image_url: str):
        self.internal_pass = image_url

