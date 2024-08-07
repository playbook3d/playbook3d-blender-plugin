import pathlib
from typing import Sequence, Optional
from dotenv import load_dotenv
import logging
import os
import requests
import datetime


class GeneralSettings:
    def __init__(self, model: int, prompt: str, strength: float) -> None:
        self.model = model
        self.scene_prompt = prompt
        self.structure_strength = strength


class MaskSettings:
    def __init__(self, prompt: str, color: str) -> None:
        self.mask_prompt = prompt
        self.color = color


class StyleTransferSettings:
    def __init__(self, strength: float) -> None:
        self.style_transfer_strength = strength


class RelightSettings:
    def __init__(self, color: str, prompt: str, angle: int) -> None:
        self.relight_color = color
        self.relight_prompt = prompt
        self.relight_angle = angle


class UpscaleSettings:
    def __init__(self, value: int) -> None:
        self.upscale_value = value


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
        general_settings: GeneralSettings,
        mask_settings1: MaskSettings,
        mask_settings2: MaskSettings,
        mask_settings3: MaskSettings,
        mask_settings4: MaskSettings,
        mask_settings5: MaskSettings,
        mask_settings6: MaskSettings,
        mask_settings7: MaskSettings,
        fixed_seed: bool,
        style_transfer_settings: StyleTransferSettings,
        relight_settings: RelightSettings,
        upscale_settings: UpscaleSettings,
        render_mode: int,
        retexture_enabled: bool,
        style_transfer_enabled: bool,
        relight_enabled: bool,
        upscale_enabled: bool,
    ) -> str:
        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {general_settings.scene_prompt} "
            )
            files = {
                "model": general_settings.model,
                "scenePrompt": general_settings.scene_prompt,
                "structureStrength": general_settings.structure_strength,
                "mask1": mask_settings1,
                "mask2": mask_settings2,
                "mask3": mask_settings3,
                "mask4": mask_settings4,
                "mask5": mask_settings5,
                "mask6": mask_settings6,
                "mask7": mask_settings7,
                "fixedSeed": fixed_seed,
                "beauty": self.beauty,
                "mask": self.mask,
                "depth": self.depth,
                "outline": self.outline,
            }

            env_file_path = pathlib.Path(__file__).parent.parent / ".env"

            # Load environment variables from the .env file
            load_dotenv(dotenv_path=env_file_path)
            url = os.getenv("BASE_URL")

            run_result = requests.post(url + "/upload-images", data=files)

            if retexture_enabled:
                self.run_retexture(general_settings.scene_prompt, url)

            if style_transfer_enabled:
                self.run_style_transfer(style_transfer_settings, url)

            if relight_enabled:
                self.run_relight(relight_settings, url)

            if upscale_enabled:
                self.run_upscale(upscale_settings)

            if run_result is not None:
                return run_result.json()
            else:
                logging.error(f"Error running workflow: {run_result}")

    #
    def run_retexture(self, prompt: str, url: str):
        # TODO: retexture
        if prompt:
            retexture_result = requests.post(
                url + "/retexture", json={"prompt": prompt}
            )
            if retexture_result is not None:
                self.internal_pass = retexture_result.json()["internal_pass"]

    #
    def run_style_transfer(
        self, style_transfer_settings: StyleTransferSettings, url: str
    ):
        # TODO: style transfer
        strength = style_transfer_settings.style_transfer_strength
        if strength:
            style_transfer_result = requests.post(
                url + "/style-transfer",
                json={"strength": strength},
            )
            if style_transfer_result is not None:
                self.internal_pass = style_transfer_result.json()["internal_pass"]

    #
    def run_relight(
        self,
        relight_settings: RelightSettings,
        url: str,
    ):
        # TODO: relight
        color = relight_settings.relight_color
        prompt = relight_settings.relight_prompt
        angle = relight_settings.relight_angle
        if color and prompt and angle:
            relight_result = requests.post(url + "/relight")
            if relight_result is not None:
                self.internal_pass = relight_result.json()["internal_pass"]

    #
    def run_upscale(self, upscale_settings: UpscaleSettings, url: str):
        # TODO: upscale
        value = upscale_settings.upscale_value
        if value:
            upscale_result = requests.post(url + "/upscale", json={"value": value})
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
