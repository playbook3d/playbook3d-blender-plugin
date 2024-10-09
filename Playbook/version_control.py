import bpy
import os
import requests
from packaging import version
from .utilities.utilities import get_env


class UpdateChecker:

    can_update = False

    @classmethod
    def check_if_version_up_to_date(cls, current_version):
        url = get_env("LATEST_VERSION_URL")
        response = requests.get(url)

        if response.status_code == 200:
            latest_version = version.parse(response.text)

            current_version = version.parse(
                f"{str(current_version[0])}.{str(current_version[1])}.{str(current_version[2])}"
            )

            print(f"Latest: {latest_version}")
            print(f"Current: {current_version}")

            if latest_version > current_version:
                cls.can_update = True

        # TODO: If current version < most up-to-date version, notify user
        return


class AutoUpdateOperator(bpy.types.Operator):
    bl_idname = "op.auto_update"
    bl_label = "Update"

    def execute(self, context):
        try:
            url = get_env("LATEST_VERSION_URL")
            print(url)

            response = requests.get(url)

            if response is not None:
                print(response)
                # print(response.json())

            return {"FINISHED"}

        except Exception as e:
            print(e)
            return {"CANCELLED"}


# def register():
