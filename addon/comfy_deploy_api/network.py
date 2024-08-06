from comfydeploy import ComfyDeploy
from comfydeploy.models import operations
from typing import Dict
import os
import logging
import requests


class ComfyDeployClient:
    def __init__(self):
        self.client = ComfyDeploy(bearer_auth=os.getenv("COMFYDEPLOY_TOKEN", ""))
        self.mask = ""
        self.depth = ""
        self.outline = ""

    async def get_render_result(self, run_id: str) -> Dict:
        return self.client.run.get(run_id=run_id).outputs

    async def get_render_status(self, run_id: str) -> str:
        return self.client.run.get(run_id=run_id).status

    async def get_render_progress(self, run_id: str) -> int:
        return self.client.run.get(run_id=run_id).progress

    async def upload_image(
        self, image_data: bytes, image_size: str, mask_type: str
    ) -> None:
        image_type = operations.Type.APPLICATION_OCTET_STREAM
        logging.info(f"Starting file upload for pass: {image_type}")
        upload_url_result = self.client.files.get_upload_url(
            type_=image_type, file_size=image_size
        )

        if upload_url_result is not None:
            match mask_type:
                case "mask":
                    self.mask = upload_url_result.file_id
                case "depth":
                    self.depth = upload_url_result.file_id
                case "outline":
                    self.outline = upload_url_result.file_id

            upload_request = requests.put(
                upload_url_result.upload_url,
                json=image_data,
                headers={"Content-Type": operations.Type.APPLICATION_OCTET_STREAM},
            )
            if upload_request.status_code != 200:
                logging.error(f"Error uploading image: {upload_request.status_code}")
            else:
                logging.info(f"Image uploaded: {image_type}")

    async def run_workflow(
        self, prompt: str, prompt_a: str, prompt_b: str, prompt_c: str, prompt_d: str
    ) -> str:
        if self.mask and self.depth and self.outline:
            logging.info(
                f"Starting workflow for prompt: {prompt} "
                f"with detailed prompt {prompt_a}, {prompt_b}, {prompt_c}, {prompt_d}"
            )
            run_result = self.client.run.create(
                request={
                    "deployment_id": os.getenv("CURRENT_WORKFLOW_ID", ""),
                    "inputs": {
                        "general_prompt": prompt,
                        "Prompt A": prompt_a,
                        "Prompt B": prompt_b,
                        "Prompt C": prompt_c,
                        "Prompt D": prompt_d,
                        "Prompt E": prompt,
                        "Mask": self.mask,
                        "Depth": self.depth,
                        "Outline": self.outline,
                    },
                }
            )

            if run_result is not None:
                return run_result.run_id
            else:
                logging.error(f"Error running workflow: {run_result}")

    async def run_test_workflow(self, prompt: str) -> str:
        if prompt:
            logging.info(f"Starting test workflow for prompt: {prompt}")
            run_result = self.client.run.create(
                request={
                    "deployment_id": os.getenv("TEST_WORKFLOW_ID", ""),
                    "inputs": {"positive_prompt": prompt},
                }
            )
            if run_result is not None:
                return run_result.run_id
            else:
                logging.error(f"Error running test workflow: {run_result}")
