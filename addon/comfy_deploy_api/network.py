import json
from typing import Sequence, Optional
import logging

import jsonpath
import requests
import datetime

baseUrl = "https://api.playbookengine.com"


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
        self.normal: Optional[bytes] = b""
        self.beauty: Optional[bytes] = b""

    async def run_workflow(
        self, prompt: str, prompt_a: str, prompt_b: str, prompt_c: str, prompt_d: str
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
            run_result = requests.post(baseUrl + "/upload-images", files=files)

            if run_result is not None:
                return run_result.json()
            else:
                logging.error(f"Error running workflow: {run_result}")

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

