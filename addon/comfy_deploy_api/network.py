from typing import Sequence, Optional
import logging
import os
import requests
import datetime

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
            model: int,
            prompt: str,
            structure_strength: int,
            prompt_a: str,
            prompt_b: str,
            prompt_c: str,
            prompt_d: str,
            prompt_e: str,
            prompt_f: str,
            prompt_g: str,
            fixed_seed: bool,
            style_transfer_strength: int,
            relight_color: str,
            relight_prompt: str,
            relight_angle: int,
            upscale_value: int,
            render_mode: int,
            retexture_enabled: bool,
            style_transfer_enabled: bool,
            relight_enabled: bool,
            upscale_enabled: bool,
    ) -> str:
        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {prompt} "
                f"with detailed prompt {prompt_a}, {prompt_b}, {prompt_c}, {prompt_d}"
            )
            files = {
                "prompt": prompt,
                "prompt_a": prompt_a,
                "prompt_b": prompt_b,
                "prompt_c": prompt_c,
                "prompt_d": prompt_d,
                "mask": self.mask,
                "depth": self.depth,
                "outline": self.outline,
            }
            run_result = requests.post(os.getenv("BASE_URL") + "/upload-images", files=files)

            if retexture_enabled:
                self.run_retexture(prompt)

            if style_transfer_enabled:
                self.run_style_transfer(style_transfer_strength)

            if relight_enabled:
                self.run_relight(relight_color, relight_prompt, relight_angle)

            if upscale_enabled:
                self.run_upscale(upscale_value)

            if run_result is not None:
                return run_result.json()
            else:
                logging.error(f"Error running workflow: {run_result}")

    def run_relight(self, color: str, prompt: str, angle: int):
        # TODO: relight
        if color and prompt and angle:
            relight_result = requests.post(os.getenv("BASE_URL") + "/relight")
            if relight_result is not None:
                self.internal_pass = relight_result.json()["internal_pass"]

    def run_upscale(self, value: int):
        # TODO: upscale
        if value:
            upscale_result = requests.post(os.getenv("BASE_URL") + "/upscale", json={"value": value})
            if upscale_result is not None:
                self.internal_pass = upscale_result.json()["internal_pass"]

    def run_style_transfer(self, strength: int):
        # TODO: style transfer
        if strength:
            style_transfer_result = requests.post(os.getenv("BASE_URL") + "/style-transfer",
                                                  json={"strength": strength})
            if style_transfer_result is not None:
                self.internal_pass = style_transfer_result.json()["internal_pass"]

    def run_retexture(self, prompt: str):
        # TODO: retexture
        if prompt:
            retexture_result = requests.post(os.getenv("BASE_URL") + "/retexture", json={"prompt": prompt})
            if retexture_result is not None:
                self.internal_pass = retexture_result.json()["internal_pass"]

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

    def save_internal_image(self, image_url: str):
        self.internal_pass = image_url

