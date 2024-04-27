from api.constants import SETTINGS_DATA, Environment
from api.models import Setting
from config import DefaultConfig


def create_default_settings():
    try:
        settings = Setting.find()
        if len(settings) > 0:
            return

        for setting in SETTINGS_DATA:
            created_setting = Setting.create(**setting)

            if DefaultConfig.ENV != Environment.TEST:
                print(f"{created_setting} was created successfully")
    except Exception as e:
        print(f"ERROR (create_default_settings): {e}")
