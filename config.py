import json

import vgamepad as vg


def get_button(button_field):
    return vg.XUSB_BUTTON.__getattr__(button_field)


class Config:

    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path) as f:
            self.data = json.load(f)

    def get_button(self, label):
        try:
            return get_button(self.data[label])
        except KeyError:
            return None

    def get_video_capture_id(self):
        return self.data.get("video_capture") or 0

    def get_max_fps(self):
        return self.data.get("max_fps") or 30

    def get_crop_value(self):
        return self.data.get("crop_value") or 0
