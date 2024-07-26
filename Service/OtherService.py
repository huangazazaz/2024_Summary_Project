from Mapper import SettingMapper
from sanic.response import json
from DTO.SettingDTO import Setting
from pydantic import ValidationError
from typing import Optional


class OtherService:

    def __init__(self):
        self.settingMapper = SettingMapper.SettingMapper()

    def update_setting(self, setting: Setting):
        return self.settingMapper.update_setting(setting)

    def add_setting(self, setting: Setting):
        return self.settingMapper.add_setting(setting)

    def get_setting(self, username):
        return self.settingMapper.get_setting(username)
